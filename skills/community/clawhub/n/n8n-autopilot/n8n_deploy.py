#!/usr/bin/env python3
"""
n8n Autopilot — Deployment Engine
API client for deploying, managing, and monitoring n8n workflows.
Author: Dr. FIRAS — https://www.linkedin.com/in/doctor-firass/
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode


class DeploymentError(Exception):
    """Raised when a deployment operation fails."""
    pass


class N8nGateway:
    """
    Low-level HTTP gateway to the n8n REST API.
    Uses only stdlib (urllib) — no requests dependency.
    """

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = (base_url or os.getenv("N8N_BASE_URL", "")).rstrip("/")
        self.api_key = api_key or os.getenv("N8N_API_KEY", "")
        if not self.api_key:
            raise DeploymentError(
                "N8N_API_KEY is not set. "
                "Get one from n8n → Settings → API, then export N8N_API_KEY=..."
            )
        if not self.base_url:
            raise DeploymentError(
                "N8N_BASE_URL is not set. "
                "Example: export N8N_BASE_URL=https://your-n8n.example.com"
            )

    def _call(self, method: str, path: str, body: Optional[dict] = None,
              params: Optional[dict] = None) -> Any:
        """Execute an API request and return parsed JSON."""
        url = f"{self.base_url}/api/v1/{path.lstrip('/')}"
        if params:
            url += "?" + urlencode({k: v for k, v in params.items() if v is not None})

        data = json.dumps(body).encode("utf-8") if body else None
        req = Request(url, data=data, method=method)
        req.add_header("X-N8N-API-KEY", self.api_key)
        req.add_header("Accept", "application/json")
        if data:
            req.add_header("Content-Type", "application/json")

        try:
            with urlopen(req) as resp:
                raw = resp.read()
                return json.loads(raw) if raw else {}
        except HTTPError as exc:
            msg = exc.read().decode("utf-8", errors="replace")
            raise DeploymentError(f"HTTP {exc.code}: {msg}") from exc
        except URLError as exc:
            raise DeploymentError(f"Connection failed: {exc.reason}") from exc

    # --- Workflow CRUD ---

    def ping(self) -> bool:
        """Check API connectivity by listing workflows (limit 1)."""
        self._call("GET", "workflows", params={"limit": "1"})
        return True

    def list_workflows(self, active_only: bool = False) -> List[Dict]:
        """Retrieve all workflows, optionally filtered to active ones."""
        params = {}
        if active_only:
            params["active"] = "true"
        result = self._call("GET", "workflows", params=params)
        # n8n returns either a list or {"data": [...]}
        if isinstance(result, list):
            return result
        return result.get("data", result.get("workflows", [result] if "id" in result else []))

    def get_workflow(self, wf_id: str) -> Dict:
        """Fetch a single workflow by ID."""
        return self._call("GET", f"workflows/{wf_id}")

    def create_workflow(self, payload: Dict) -> Dict:
        """
        Create a new workflow on the n8n instance.
        Strips read-only fields that the API rejects on creation.
        """
        sanitized = {k: v for k, v in payload.items() if k not in ("id", "active", "createdAt", "updatedAt")}
        return self._call("POST", "workflows", body=sanitized)

    def patch_workflow(self, wf_id: str, updates: Dict) -> Dict:
        """Apply partial updates to a workflow."""
        return self._call("PATCH", f"workflows/{wf_id}", body=updates)

    def remove_workflow(self, wf_id: str) -> Dict:
        """Delete a workflow permanently."""
        return self._call("DELETE", f"workflows/{wf_id}")

    def set_active(self, wf_id: str, active: bool) -> Dict:
        """Toggle workflow active state."""
        return self.patch_workflow(wf_id, {"active": active})

    # --- Execution ---

    def trigger_execution(self, wf_id: str, payload: Optional[Dict] = None) -> Dict:
        """Manually trigger a workflow, optionally with input data."""
        body = {}
        if payload:
            body["data"] = payload
        return self._call("POST", f"workflows/{wf_id}/execute", body=body)

    def list_executions(self, wf_id: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """List recent executions, optionally scoped to a workflow."""
        params = {"limit": str(limit)}
        if wf_id:
            params["workflowId"] = wf_id
        result = self._call("GET", "executions", params=params)
        if isinstance(result, list):
            return result
        return result.get("data", result.get("results", []))

    def get_execution(self, exec_id: str) -> Dict:
        """Fetch full details for one execution."""
        return self._call("GET", f"executions/{exec_id}")

    # --- Statistics ---

    def compute_stats(self, wf_id: str, days: int = 7) -> Dict:
        """
        Compute execution statistics from recent history.
        Returns success/failure counts, rate, and top error messages.
        """
        executions = self.list_executions(wf_id=wf_id, limit=200)
        total = len(executions)
        ok = 0
        ko = 0
        errors: Dict[str, int] = {}

        for ex in executions:
            if ex.get("finished") or ex.get("status") == "success":
                ok += 1
            else:
                ko += 1
                err_msg = (
                    ex.get("data", {})
                    .get("resultData", {})
                    .get("error", {})
                    .get("message", "Unknown")
                )
                errors[err_msg] = errors.get(err_msg, 0) + 1

        return {
            "workflow_id": wf_id,
            "period_days": days,
            "total": total,
            "succeeded": ok,
            "failed": ko,
            "success_rate_pct": round(ok / total * 100, 1) if total else 0.0,
            "top_errors": dict(sorted(errors.items(), key=lambda x: -x[1])[:5]),
        }


class DeployPipeline:
    """
    High-level deployment operations that combine gateway calls
    with local validation for a smooth push workflow.
    """

    def __init__(self, gateway: Optional[N8nGateway] = None):
        self.gw = gateway or N8nGateway()

    def push(self, workflow_data: Dict, activate: bool = False) -> Dict:
        """
        Deploy a workflow: create on the instance, optionally activate.
        Returns the created workflow with its server-assigned ID.
        """
        created = self.gw.create_workflow(workflow_data)
        wf_id = created.get("id")
        if not wf_id:
            raise DeploymentError("Server did not return a workflow ID after creation.")

        if activate:
            self.gw.set_active(wf_id, True)
            created["active"] = True

        return created

    def push_from_file(self, filepath: str, activate: bool = False) -> Dict:
        """Load a JSON file and deploy it."""
        with open(filepath, "r") as fh:
            data = json.load(fh)
        return self.push(data, activate=activate)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _pretty(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False, default=str)


def main():
    ap = argparse.ArgumentParser(
        prog="n8n_deploy",
        description="n8n Autopilot — Deploy & manage workflows (by Dr. FIRAS)",
    )
    sub = ap.add_subparsers(dest="command", required=True)

    # ping
    sub.add_parser("ping", help="Check API connectivity")

    # ls
    p_ls = sub.add_parser("ls", help="List workflows")
    p_ls.add_argument("--active", action="store_true", help="Active only")

    # push
    p_push = sub.add_parser("push", help="Deploy workflow from JSON file")
    p_push.add_argument("--file", required=True, help="Path to workflow JSON")
    p_push.add_argument("--activate", action="store_true", help="Activate after creation")

    # inspect
    p_ins = sub.add_parser("inspect", help="Show workflow details")
    p_ins.add_argument("--id", required=True)

    # on / off
    p_on = sub.add_parser("on", help="Activate workflow")
    p_on.add_argument("--id", required=True)
    p_off = sub.add_parser("off", help="Deactivate workflow")
    p_off.add_argument("--id", required=True)

    # run
    p_run = sub.add_parser("run", help="Trigger manual execution")
    p_run.add_argument("--id", required=True)
    p_run.add_argument("--payload", default=None, help="JSON input data")

    # history
    p_hist = sub.add_parser("history", help="List recent executions")
    p_hist.add_argument("--id", default=None, help="Workflow ID (optional)")
    p_hist.add_argument("--limit", type=int, default=10)

    # exec-detail
    p_ed = sub.add_parser("exec-detail", help="Execution details")
    p_ed.add_argument("--id", required=True, help="Execution ID")

    # stats
    p_st = sub.add_parser("stats", help="Execution statistics")
    p_st.add_argument("--id", required=True)
    p_st.add_argument("--days", type=int, default=7)

    # rm
    p_rm = sub.add_parser("rm", help="Delete a workflow")
    p_rm.add_argument("--id", required=True)

    args = ap.parse_args()

    try:
        gw = N8nGateway()
        pipe = DeployPipeline(gw)

        if args.command == "ping":
            gw.ping()
            print(f"Connected to {gw.base_url}")

        elif args.command == "ls":
            wfs = gw.list_workflows(active_only=args.active)
            for wf in wfs:
                status = "ON " if wf.get("active") else "OFF"
                print(f"[{status}] {wf.get('id'):>6}  {wf.get('name', '(unnamed)')}")

        elif args.command == "push":
            result = pipe.push_from_file(args.file, activate=args.activate)
            print(f"Deployed: id={result['id']}  name={result.get('name')}")
            if args.activate:
                print("Workflow is now ACTIVE.")

        elif args.command == "inspect":
            print(_pretty(gw.get_workflow(args.id)))

        elif args.command == "on":
            gw.set_active(args.id, True)
            print(f"Workflow {args.id} activated.")

        elif args.command == "off":
            gw.set_active(args.id, False)
            print(f"Workflow {args.id} deactivated.")

        elif args.command == "run":
            payload = json.loads(args.payload) if args.payload else None
            result = gw.trigger_execution(args.id, payload)
            print(_pretty(result))

        elif args.command == "history":
            execs = gw.list_executions(wf_id=args.id, limit=args.limit)
            for ex in execs:
                fin = "OK" if ex.get("finished") or ex.get("status") == "success" else "FAIL"
                print(f"  {ex.get('id'):>8}  [{fin:4}]  {ex.get('startedAt', '?')}")

        elif args.command == "exec-detail":
            print(_pretty(gw.get_execution(args.id)))

        elif args.command == "stats":
            print(_pretty(gw.compute_stats(args.id, days=args.days)))

        elif args.command == "rm":
            gw.remove_workflow(args.id)
            print(f"Workflow {args.id} deleted.")

    except DeploymentError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
