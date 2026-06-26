#!/usr/bin/env python3
"""Run a CadQuery model script and emit a structured JSON result."""

from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
import sys
import time


def sibling(path: str, suffix: str) -> str:
    base, _ = os.path.splitext(path)
    return base + suffix


def new_outputs(directory: str, started_at: float, extensions: tuple[str, ...]) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {ext: [] for ext in extensions}
    for ext in extensions:
        candidates: list[tuple[float, str]] = []
        for path in glob.glob(os.path.join(directory, f"*.{ext}")):
            try:
                mtime = os.path.getmtime(path)
            except OSError:
                continue
            if mtime >= started_at:
                candidates.append((mtime, path))
        candidates.sort(reverse=True)
        found[ext] = [path for _, path in candidates]
    return found


def process_meshes(stls: list[str], make_preview: bool, strict: bool, views: str) -> tuple[list[str], bool | None, str | None]:
    from mesh_io import load_mesh

    previews: list[str] = []
    watertight: list[bool] = []

    for stl_path in stls:
        try:
            mesh = load_mesh(stl_path)
        except Exception as exc:
            return previews, None, f"Mesh load failed for {stl_path}: {exc}"

        wt = bool(mesh.is_watertight)
        watertight.append(wt)
        if strict and not wt:
            return previews, False, f"Mesh {stl_path} is not watertight"

        if make_preview:
            import preview

            out_path = sibling(stl_path, "_preview.png")
            try:
                preview.render(mesh, out_path, views=views)
            except Exception as exc:
                return previews, all(watertight) if watertight else None, f"Preview failed for {stl_path}: {exc}"
            previews.append(out_path)

    return previews, all(watertight) if watertight else None, None


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a CadQuery model and report JSON")
    parser.add_argument("script", help="Path to the CadQuery script")
    parser.add_argument("--preview", action="store_true", help="Render preview images for exported STL files")
    parser.add_argument("--strict", action="store_true", help="Fail if the mesh is not watertight or no STL was produced")
    parser.add_argument("--views", choices=["iso", "multi"], default="multi")
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()

    script_path = os.path.abspath(args.script)
    script_dir = os.path.dirname(script_path) or "."
    started_at = time.time()

    result = {
        "success": False,
        "script": args.script,
        "stls": [],
        "stl": None,
        "previews": [],
        "preview": None,
        "threemfs": [],
        "threemf": None,
        "watertight": None,
        "stdout": "",
        "stderr": "",
        "returncode": -1,
    }

    try:
        proc = subprocess.run(
            [sys.executable, script_path],
            cwd=script_dir,
            capture_output=True,
            text=True,
            timeout=args.timeout,
        )
    except subprocess.TimeoutExpired as exc:
        result["stderr"] = f"Timeout after {args.timeout}s: {exc}"
        print(json.dumps(result, indent=2))
        return 3
    except FileNotFoundError as exc:
        result["stderr"] = f"Failed to launch interpreter: {exc}"
        print(json.dumps(result, indent=2))
        return 2

    result["stdout"] = proc.stdout
    result["stderr"] = proc.stderr
    result["returncode"] = proc.returncode
    result["success"] = proc.returncode == 0

    if result["success"]:
        outputs = new_outputs(script_dir, started_at, ("stl", "3mf"))
        result["stls"] = outputs["stl"]
        result["threemfs"] = outputs["3mf"]

    if args.strict and result["success"] and not result["stls"]:
        result["success"] = False
        result["stderr"] = (result["stderr"] + "\n" if result["stderr"] else "") + "No STL files were produced"

    if result["success"] and result["stls"] and (args.preview or args.strict):
        previews, watertight, error = process_meshes(result["stls"], args.preview, args.strict, args.views)
        result["previews"] = previews
        result["watertight"] = watertight
        if error:
            result["success"] = False
            result["stderr"] = (result["stderr"] + "\n" if result["stderr"] else "") + error

    result["stl"] = result["stls"][0] if result["stls"] else None
    result["preview"] = result["previews"][0] if result["previews"] else None
    result["threemf"] = result["threemfs"][0] if result["threemfs"] else None

    print(json.dumps(result, indent=2))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
