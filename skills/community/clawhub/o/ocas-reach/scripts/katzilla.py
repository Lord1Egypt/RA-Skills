#!/usr/bin/env python3
"""
Katzilla API helper — US Government data backbone for AI agents.

Usage:
  python3 katzilla.py agents                           # List all agents
  python3 katzilla.py query <agent> <action> [params]  # Execute an action
  python3 katzilla.py mock <agent> <action> [params]   # Free mock mode

Examples:
  python3 katzilla.py query hazards usgs-earthquakes '{"minMagnitude":5,"limit":3}'
  python3 katzilla.py query government congress-bills '{"query":"climate","limit":3}'
  python3 katzilla.py query health fda-recalls '{"search":"peanut","limit":5}'
  python3 katzilla.py query economic fred-gdp '{"limit":5}'
  python3 katzilla.py query crime fbi-wanted '{"limit":3}'
  python3 katzilla.py mock hazards usgs-earthquakes '{}'
"""

import os
import sys
import json
import urllib.request
import urllib.error

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 katzilla.py")
    sys.exit(0)


API_BASE = "https://api.katzilla.dev"
KZ_KEY = os.environ.get("KZ_KEY", "")

def api_request(method, path, body=None):
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": KZ_KEY,
    }
    url = f"{API_BASE}{path}"
    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode('utf-8')}"}
    except urllib.error.URLError as e:
        return {"error": str(e.reason)}

def list_agents():
    """List all available agents from the API."""
    result = api_request("GET", "/agents")
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    agents = result.get("data", result)
    print(f"{'AGENT':30s} {'HANDLE':20s} {'ACTIONS':8s} {'CATEGORIES'}")
    print("-" * 80)
    for a in agents:
        if isinstance(a, dict):
            handle = a.get("handle", "?")
            name = a.get("name", "?")[:29]
            actions = str(a.get("actionCount", a.get("actions", [])))
            cats = ", ".join(a.get("categories", []))[:30]
            print(f"{name:30s} {handle:20s} {actions:8s} {cats}")

def query_action(agent_id, action_id, params=None):
    """Execute an action on an agent."""
    path = f"/agents/{agent_id}/actions/{action_id}"
    result = api_request("POST", path, params or {})
    if "error" in result:
        print(f"Error: {result['error']}")
        return
    print(f"Agent:   {result.get('meta', {}).get('agent', '?')}")
    print(f"Action:  {result.get('meta', {}).get('action', '?')}")
    print(f"Cache:   {result.get('meta', {}).get('cacheStatus', '?')}")
    print(f"Credits: {result.get('meta', {}).get('creditsCharged', 0)}")
    print(f"Source:  {result.get('citation', {}).get('source_name', '?')}")
    print(f"License: {result.get('citation', {}).get('license', '?')}")
    print(f"Quality: {result.get('quality', {}).get('confidence', '?')} ({result.get('quality', {}).get('certainty_score', 0)})")
    print()
    data = result.get("data", {})
    print(json.dumps(data, indent=2))

def mock_action(agent_id, action_id, params=None):
    """Mock mode — no upstream hit, free on every plan."""
    body = params or {}
    body["_mock"] = True
    return query_action(agent_id, action_id, body)

def main():
    if not KZ_KEY:
        print("Error: KZ_KEY environment variable not set.")
        print("Add to ~/.hermes/.env: KZ_KEY=kz_live_...")
        sys.exit(1)

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "agents":
        list_agents()
    elif cmd == "query":
        if len(sys.argv) < 4:
            print("Usage: katzilla.py query <agent> <action> [json_params]")
            sys.exit(1)
        agent = sys.argv[2]
        action = sys.argv[3]
        params = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
        query_action(agent, action, params)
    elif cmd == "mock":
        if len(sys.argv) < 4:
            print("Usage: katzilla.py mock <agent> <action> [json_params]")
            sys.exit(1)
        agent = sys.argv[2]
        action = sys.argv[3]
        params = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
        mock_action(agent, action, params)
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
