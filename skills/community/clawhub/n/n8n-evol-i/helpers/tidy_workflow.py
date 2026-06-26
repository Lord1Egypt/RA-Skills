#!/usr/bin/env python3
"""
Tidy workflow node positions using @n8n/workflow-sdk's layoutWorkflowJSON.

Usage:
    python3 helpers/tidy_workflow.py --workspace <ws> --workflow-key <key> [--in-place]

If Node.js is unavailable or the shim subprocess fails for any reason, falls back
to a pure-Python BFS layout that approximates left-to-right depth assignment.

SDK pin: @n8n/workflow-sdk@stable (0.10.2) — licensed under n8n Sustainable Use License.
"""
import argparse
import json
import shutil
import subprocess
import sys
from collections import deque
from pathlib import Path

_HARNESS_ROOT = Path(__file__).resolve().parent.parent
_SHIM = _HARNESS_ROOT / "helpers" / "tidy_shim.mjs"
_SDK_VERSION = "0.10.2"
_STICKY_TYPE = "n8n-nodes-base.stickyNote"
_START_X = 240
_START_Y = 300
_H_GAP = 220
_V_GAP = 120


def _ensure_sdk() -> bool:
    """Install @n8n/workflow-sdk into helpers/node_modules if not already present. Returns True on success."""
    helpers_dir = _HARNESS_ROOT / "helpers"
    sdk_dir = helpers_dir / "node_modules" / "@n8n" / "workflow-sdk"
    if sdk_dir.exists():
        return True
    if not shutil.which("node") or not shutil.which("npm"):
        return False
    result = subprocess.run(
        ["npm", "install", "--prefix", str(helpers_dir),
         f"@n8n/workflow-sdk@{_SDK_VERSION}",
         "--silent", "--no-fund", "--no-audit"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"[tidy_workflow] npm install failed:\n{result.stderr}", file=sys.stderr)
        return False
    return sdk_dir.exists()


def _layout_via_shim(workflow: dict) -> dict | None:
    """Run the Node.js shim. Returns the laid-out workflow dict, or None on any failure."""
    if not shutil.which("node"):
        return None
    if not _ensure_sdk():
        return None
    try:
        result = subprocess.run(
            ["node", str(_SHIM)],
            input=json.dumps(workflow),
            capture_output=True,
            text=True,
            timeout=60,
        )
    except Exception as exc:
        print(f"[tidy_workflow] shim subprocess error: {exc}", file=sys.stderr)
        return None
    if result.returncode != 0:
        print(f"[tidy_workflow] shim exited {result.returncode}: {result.stderr}", file=sys.stderr)
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print(f"[tidy_workflow] shim output not valid JSON: {exc}", file=sys.stderr)
        return None


def _bfs_layout(workflow: dict) -> dict:
    """
    Pure-Python BFS layout fallback.

    Sticky notes are left untouched. All other nodes are assigned
    [start_x + depth * H_GAP, start_y + branch * V_GAP].

    Pure-cycle graphs (no root nodes) fall back to insertion-order layout.
    Disconnected components each get their own row offset.
    """
    nodes = workflow.get("nodes", [])
    connections = workflow.get("connections", {})

    non_sticky = [n for n in nodes if n.get("type") != _STICKY_TYPE]

    if not non_sticky:
        return workflow

    # Build adjacency: name -> set of child names
    children: dict[str, set[str]] = {n["name"]: set() for n in non_sticky}
    in_degree: dict[str, int] = {n["name"]: 0 for n in non_sticky}
    name_set = {n["name"] for n in non_sticky}

    for src_name, output_types in connections.items():
        if src_name not in name_set:
            continue
        for _output_type, output_branches in output_types.items():
            if not isinstance(output_branches, list):
                continue
            for branch in output_branches:
                if not isinstance(branch, list):
                    continue
                for edge in branch:
                    dst = edge.get("node", "")
                    if dst in name_set and dst != src_name:
                        children[src_name].add(dst)
                        in_degree[dst] = in_degree.get(dst, 0) + 1

    # Assign positions
    positions: dict[str, list[int]] = {}
    visited: set[str] = set()
    component_row = 0  # row offset per disconnected component

    def _bfs_from_roots(roots: list[str]) -> None:
        nonlocal component_row
        queue: deque[tuple[str, int]] = deque()
        depth_count: dict[int, int] = {}
        local_visited: set[str] = set()

        for r in roots:
            queue.append((r, 0))
            local_visited.add(r)

        while queue:
            name, depth = queue.popleft()
            if name in visited:
                continue
            visited.add(name)
            branch = depth_count.get(depth, 0)
            depth_count[depth] = branch + 1
            positions[name] = [
                _START_X + depth * _H_GAP,
                _START_Y + (component_row + branch) * _V_GAP,
            ]
            for child in sorted(children.get(name, [])):
                if child not in local_visited:
                    local_visited.add(child)
                    queue.append((child, depth + 1))

        if depth_count:
            component_row += max(depth_count.values())

    insertion_order = [n["name"] for n in non_sticky]

    # Collect roots (in-degree 0)
    roots = [n for n in insertion_order if in_degree.get(n, 0) == 0]

    if roots:
        _bfs_from_roots(roots)
        # Handle any remaining unvisited nodes (disconnected components)
        remaining = [n for n in insertion_order if n not in visited]
        while remaining:
            component_row += 1
            next_root = remaining[0]
            reachable = {next_root}
            q: deque[str] = deque([next_root])
            while q:
                cur = q.popleft()
                for child in children.get(cur, []):
                    if child not in reachable:
                        reachable.add(child)
                        q.append(child)
            comp_roots = [n for n in remaining if in_degree.get(n, 0) == 0 and n in reachable]
            if not comp_roots:
                comp_roots = [n for n in remaining if n in reachable]
            _bfs_from_roots(comp_roots)
            remaining = [n for n in insertion_order if n not in visited]
    else:
        # Pure-cycle graph: assign insertion-order layout, no crash
        for i, name in enumerate(insertion_order):
            positions[name] = [_START_X + i * _H_GAP, _START_Y]
            visited.add(name)

    # Apply positions back
    result_nodes = []
    for node in nodes:
        n = dict(node)
        if n.get("type") != _STICKY_TYPE and n["name"] in positions:
            n["position"] = positions[n["name"]]
        result_nodes.append(n)

    return {**workflow, "nodes": result_nodes}


def tidy(workflow: dict) -> dict:
    """Apply tidy layout: try SDK shim first, fall back to BFS.

    Sticky note positions are always preserved — the SDK moves them, so we
    snapshot before layout and restore after.
    """
    sticky_positions = {
        n["name"]: n["position"]
        for n in workflow.get("nodes", [])
        if n.get("type") == _STICKY_TYPE
    }
    laid = _layout_via_shim(workflow)
    if laid is None:
        print("[tidy_workflow] using Python BFS fallback", file=sys.stderr)
        laid = _bfs_layout(workflow)
    if sticky_positions:
        restored_nodes = []
        for n in laid.get("nodes", []):
            if n.get("type") == _STICKY_TYPE and n["name"] in sticky_positions:
                n = {**n, "position": sticky_positions[n["name"]]}
            restored_nodes.append(n)
        laid = {**laid, "nodes": restored_nodes}
    return laid


def _load_workflow(workspace: Path, key: str) -> tuple[Path, dict]:
    template_dir = workspace / "n8n-workflows-template"
    path = template_dir / f"{key}.template.json"
    if not path.exists():
        sys.exit(f"[tidy_workflow] template not found: {path}")
    with open(path) as f:
        return path, json.load(f)


def main() -> None:
    parser = argparse.ArgumentParser(description="Tidy n8n workflow node positions.")
    parser.add_argument("--workspace", required=True, help="Path to n8n-evol-I workspace directory")
    parser.add_argument("--workflow-key", required=True, help="Workflow key (filename stem without .template.json)")
    parser.add_argument("--in-place", action="store_true", help="Write result back to template file (default: print to stdout)")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    path, workflow = _load_workflow(workspace, args.workflow_key)
    result = tidy(workflow)

    if args.in_place:
        with open(path, "w") as f:
            json.dump(result, f, indent=2)
            f.write("\n")
        print(f"[tidy_workflow] wrote {path}", file=sys.stderr)
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
