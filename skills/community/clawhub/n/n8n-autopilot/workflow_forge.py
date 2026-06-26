#!/usr/bin/env python3
"""
n8n Autopilot — Workflow Forge
Programmatic builder for constructing n8n workflow JSON.
Provides a fluent API to compose nodes, wire connections,
and export ready-to-import JSON.

Author: Dr. FIRAS — https://www.linkedin.com/in/doctor-firass/
"""

import json
import uuid
import sys
import argparse
from typing import Optional, Dict, List, Any


def _uuid() -> str:
    return str(uuid.uuid4())


class Node:
    """Represents a single n8n node with its configuration."""

    def __init__(
        self,
        name: str,
        node_type: str,
        type_version: int = 1,
        parameters: Optional[Dict] = None,
        credentials: Optional[Dict] = None,
        position: Optional[List[int]] = None,
    ):
        self.id = _uuid()
        self.name = name
        self.node_type = node_type
        self.type_version = type_version
        self.parameters = parameters or {}
        self.credentials = credentials or {}
        self.position = position or [0, 0]

    def to_dict(self) -> Dict:
        out = {
            "id": self.id,
            "name": self.name,
            "type": self.node_type,
            "typeVersion": self.type_version,
            "position": self.position,
            "parameters": self.parameters,
        }
        if self.credentials:
            out["credentials"] = self.credentials
        return out


class Workflow:
    """
    Fluent builder for assembling a complete n8n workflow.

    Usage:
        wf = (Workflow("My Flow")
              .add_webhook_trigger("/incoming", method="POST")
              .add_set_node("Extract", {"email": "={{ $json.email }}"})
              .add_http_request("Call API", url="https://api.example.com/users",
                                method="POST", body_expr='={{ JSON.stringify($json) }}')
              .add_respond_webhook("Reply", status=200)
              .chain_all()
              )
        print(wf.to_json())
    """

    def __init__(self, name: str, execution_timeout: Optional[int] = None):
        self.name = name
        self._nodes: List[Node] = []
        self._connections: Dict[str, Dict] = {}
        self._x_cursor = 300
        self._y_cursor = 300
        self._settings: Dict[str, Any] = {"executionOrder": "v1"}
        if execution_timeout:
            self._settings["executionTimeout"] = execution_timeout

    # --- Node factories ---

    def add_node(self, node: Node) -> "Workflow":
        """Add a pre-built Node object."""
        if node.position == [0, 0]:
            node.position = [self._x_cursor, self._y_cursor]
            self._x_cursor += 220
        self._nodes.append(node)
        return self

    def add_manual_trigger(self, name: str = "Start") -> "Workflow":
        return self.add_node(Node(name, "n8n-nodes-base.manualTrigger", 1))

    def add_webhook_trigger(
        self, path: str, method: str = "POST", name: str = "Webhook",
        response_mode: str = "responseNode"
    ) -> "Workflow":
        return self.add_node(Node(
            name, "n8n-nodes-base.webhook", 2,
            parameters={
                "httpMethod": method,
                "path": path.lstrip("/"),
                "responseMode": response_mode,
                "options": {},
            },
        ))

    def add_schedule_trigger(
        self, name: str = "Schedule", field: str = "hours", interval: int = 1
    ) -> "Workflow":
        return self.add_node(Node(
            name, "n8n-nodes-base.scheduleTrigger", 1,
            parameters={
                "rule": {"interval": [{"field": field, f"{field}Interval": interval}]}
            },
        ))

    def add_set_node(self, name: str, assignments: Dict[str, str]) -> "Workflow":
        """
        Add a Set node that maps fields.
        `assignments` is a dict of {output_field: expression_or_value}.
        """
        items = []
        for idx, (field, value) in enumerate(assignments.items()):
            items.append({
                "id": f"f{idx}",
                "name": field,
                "value": value,
                "type": "string",
            })
        return self.add_node(Node(
            name, "n8n-nodes-base.set", 3,
            parameters={
                "mode": "manual",
                "assignments": {"assignments": items},
                "options": {},
            },
        ))

    def add_code_node(self, name: str, code: str, language: str = "javaScript") -> "Workflow":
        return self.add_node(Node(
            name, "n8n-nodes-base.code", 2,
            parameters={"language": language, "jsCode": code},
        ))

    def add_http_request(
        self,
        name: str,
        url: str,
        method: str = "GET",
        body_expr: Optional[str] = None,
        auth_type: str = "none",
        credential_name: Optional[str] = None,
    ) -> "Workflow":
        params: Dict[str, Any] = {
            "method": method,
            "url": url,
            "authentication": auth_type,
            "options": {},
        }
        if body_expr and method in ("POST", "PUT", "PATCH"):
            params["sendBody"] = True
            params["specifyBody"] = "json"
            params["jsonBody"] = body_expr
        creds = {}
        if credential_name and auth_type != "none":
            creds = {auth_type: {"id": "1", "name": credential_name}}
        return self.add_node(Node(
            name, "n8n-nodes-base.httpRequest", 4,
            parameters=params, credentials=creds,
        ))

    def add_if_node(
        self,
        name: str,
        left: str,
        operator: str,
        right: str,
        op_type: str = "string",
    ) -> "Workflow":
        return self.add_node(Node(
            name, "n8n-nodes-base.if", 2,
            parameters={
                "conditions": {
                    "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict"},
                    "conditions": [{
                        "id": _uuid(),
                        "leftValue": left,
                        "rightValue": right,
                        "operator": {"type": op_type, "operation": operator},
                    }],
                    "combinator": "and",
                },
                "options": {},
            },
        ))

    def add_respond_webhook(
        self, name: str = "Reply", status: int = 200, body_expr: str = '={{ JSON.stringify($json) }}'
    ) -> "Workflow":
        return self.add_node(Node(
            name, "n8n-nodes-base.respondToWebhook", 1,
            parameters={
                "respondWith": "json",
                "responseBody": body_expr,
                "options": {"responseCode": status},
            },
        ))

    def add_slack_message(
        self, name: str, channel: str, text: str, credential_name: str = "Slack"
    ) -> "Workflow":
        return self.add_node(Node(
            name, "n8n-nodes-base.slack", 2,
            parameters={
                "resource": "message",
                "operation": "post",
                "channel": channel,
                "text": text,
                "options": {},
            },
            credentials={"slackApi": {"id": "1", "name": credential_name}},
        ))

    def add_noop(self, name: str = "End") -> "Workflow":
        return self.add_node(Node(name, "n8n-nodes-base.noOp", 1))

    # --- Wiring ---

    def connect(self, source: str, target: str, source_output: int = 0) -> "Workflow":
        """Wire source node → target node on the given output index."""
        entry = self._connections.setdefault(source, {"main": []})
        main = entry["main"]
        # Ensure enough output slots
        while len(main) <= source_output:
            main.append([])
        main[source_output].append({"node": target, "type": "main", "index": 0})
        return self

    def chain_all(self) -> "Workflow":
        """Wire all nodes sequentially in the order they were added."""
        for i in range(len(self._nodes) - 1):
            self.connect(self._nodes[i].name, self._nodes[i + 1].name)
        return self

    def chain(self, *names: str) -> "Workflow":
        """Wire a specific sequence of node names."""
        for i in range(len(names) - 1):
            self.connect(names[i], names[i + 1])
        return self

    def branch(self, source: str, true_target: str, false_target: str) -> "Workflow":
        """Wire an IF node's two outputs."""
        self.connect(source, true_target, source_output=0)
        self.connect(source, false_target, source_output=1)
        return self

    # --- Layout ---

    def auto_layout(self, start_x: int = 300, start_y: int = 300, gap_x: int = 220, gap_y: int = 200):
        """
        Reposition all nodes in a left-to-right layout.
        Simple topological ordering with vertical offset for branches.
        """
        # Build adjacency
        adj: Dict[str, List[str]] = {}
        for src, conn in self._connections.items():
            for output_list in conn.get("main", []):
                for link in output_list:
                    adj.setdefault(src, []).append(link["node"])

        # BFS from trigger
        name_to_node = {n.name: n for n in self._nodes}
        trigger_names = [n.name for n in self._nodes if "trigger" in n.node_type.lower() or "Trigger" in n.node_type]
        queue = list(trigger_names) or ([self._nodes[0].name] if self._nodes else [])

        visited = set()
        col = 0
        while queue:
            next_queue = []
            row = 0
            for name in queue:
                if name in visited:
                    continue
                visited.add(name)
                if name in name_to_node:
                    name_to_node[name].position = [start_x + col * gap_x, start_y + row * gap_y]
                    row += 1
                for child in adj.get(name, []):
                    if child not in visited:
                        next_queue.append(child)
            col += 1
            queue = next_queue

        # Place any unvisited nodes
        for n in self._nodes:
            if n.name not in visited:
                n.position = [start_x + col * gap_x, start_y]
                col += 1

        return self

    # --- Export ---

    def to_dict(self) -> Dict:
        self.auto_layout()
        return {
            "name": self.name,
            "nodes": [n.to_dict() for n in self._nodes],
            "connections": self._connections,
            "active": False,
            "settings": self._settings,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def save(self, filepath: str) -> str:
        """Write the workflow JSON to a file and return the path."""
        with open(filepath, "w") as fh:
            fh.write(self.to_json())
        return filepath

    def deploy(self, activate: bool = False) -> Dict:
        """Push the workflow to the configured n8n instance."""
        from n8n_deploy import DeployPipeline
        pipe = DeployPipeline()
        return pipe.push(self.to_dict(), activate=activate)


# ---------------------------------------------------------------------------
# Recipe loader — build from YAML/JSON spec
# ---------------------------------------------------------------------------

def build_from_recipe(recipe_path: str) -> Workflow:
    """
    Build a workflow from a declarative recipe file (JSON or YAML).
    Recipe format:
    {
      "name": "My Workflow",
      "timeout": 300,
      "nodes": [
        {"kind": "webhook", "name": "Hook", "path": "/hook"},
        {"kind": "set", "name": "Parse", "fields": {"email": "={{ $json.email }}"}},
        {"kind": "http", "name": "Fetch", "url": "...", "method": "GET"},
        ...
      ],
      "wiring": "chain" | [["A","B"], ["B","C"]]
    }
    """
    with open(recipe_path, "r") as fh:
        content = fh.read()

    # Try YAML first, fall back to JSON
    try:
        import yaml
        recipe = yaml.safe_load(content)
    except (ImportError, Exception):
        recipe = json.loads(content)

    wf = Workflow(recipe.get("name", "Untitled"), execution_timeout=recipe.get("timeout"))

    kind_map = {
        "manual": lambda n: wf.add_manual_trigger(n.get("name", "Start")),
        "webhook": lambda n: wf.add_webhook_trigger(
            n.get("path", "/hook"), n.get("method", "POST"), n.get("name", "Webhook")
        ),
        "schedule": lambda n: wf.add_schedule_trigger(
            n.get("name", "Schedule"), n.get("field", "hours"), n.get("interval", 1)
        ),
        "set": lambda n: wf.add_set_node(n["name"], n.get("fields", {})),
        "code": lambda n: wf.add_code_node(n["name"], n.get("code", "return $input.all();")),
        "http": lambda n: wf.add_http_request(
            n["name"], n["url"], n.get("method", "GET"), n.get("body")
        ),
        "if": lambda n: wf.add_if_node(
            n["name"], n["left"], n.get("op", "equals"), n["right"]
        ),
        "respond": lambda n: wf.add_respond_webhook(n.get("name", "Reply")),
        "slack": lambda n: wf.add_slack_message(n["name"], n["channel"], n["text"]),
        "noop": lambda n: wf.add_noop(n.get("name", "End")),
    }

    for node_spec in recipe.get("nodes", []):
        kind = node_spec.get("kind", "").lower()
        builder = kind_map.get(kind)
        if builder:
            builder(node_spec)
        else:
            # Generic node fallback
            wf.add_node(Node(
                node_spec["name"],
                node_spec["type"],
                node_spec.get("version", 1),
                node_spec.get("parameters", {}),
                node_spec.get("credentials", {}),
            ))

    wiring = recipe.get("wiring", "chain")
    if wiring == "chain":
        wf.chain_all()
    elif isinstance(wiring, list):
        for pair in wiring:
            if len(pair) == 2:
                wf.connect(pair[0], pair[1])
            elif len(pair) == 3:
                wf.connect(pair[0], pair[1], source_output=pair[2])

    return wf


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        prog="workflow_forge",
        description="n8n Autopilot — Workflow Forge (by Dr. FIRAS)",
    )
    sub = ap.add_subparsers(dest="command", required=True)

    p_build = sub.add_parser("build", help="Build workflow from a recipe file")
    p_build.add_argument("--recipe", required=True, help="Path to recipe JSON/YAML")
    p_build.add_argument("--output", default=None, help="Write JSON to file")
    p_build.add_argument("--deploy", action="store_true", help="Deploy to n8n instance")
    p_build.add_argument("--activate", action="store_true", help="Activate after deploy")

    args = ap.parse_args()

    if args.command == "build":
        wf = build_from_recipe(args.recipe)

        if args.output:
            wf.save(args.output)
            print(f"Saved to {args.output}")

        if args.deploy:
            result = wf.deploy(activate=args.activate)
            print(f"Deployed: id={result['id']}  name={result.get('name')}")
        elif not args.output:
            print(wf.to_json())


if __name__ == "__main__":
    main()
