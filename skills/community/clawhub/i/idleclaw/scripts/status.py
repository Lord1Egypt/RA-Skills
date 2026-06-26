"""IdleClaw Status — Check network health and available models."""

import sys

import httpx

from config import get_server_url


def check_status(server_url: str) -> None:
    """Query server health and model endpoints."""
    print("IdleClaw Network Status")
    print("=======================")
    print(f"Server: {server_url}")
    print()

    # Check health
    try:
        health_resp = httpx.get(f"{server_url}/health", timeout=10)
        health_resp.raise_for_status()
        health = health_resp.json()
    except (httpx.ConnectError, httpx.HTTPError):
        print("Status:  OFFLINE")
        print()
        print(f"Cannot reach server at {server_url}")
        print("Check that the IdleClaw server is running.")
        print("You can set IDLECLAW_SERVER to point to a different server.")
        sys.exit(1)

    node_count = health.get("node_count", 0)
    uptime = health.get("uptime_seconds", 0)

    print(f"Status:  ONLINE")
    print(f"Nodes:   {node_count} connected")
    print(f"Uptime:  {format_uptime(uptime)}")
    print()

    # Check models
    try:
        models_resp = httpx.get(f"{server_url}/api/models", timeout=10)
        models_resp.raise_for_status()
        models_data = models_resp.json()
        models = models_data.get("models", [])
    except (httpx.ConnectError, httpx.HTTPError):
        print("Models:  (unable to fetch)")
        return

    if models:
        print(f"Available Models ({len(models)}):")
        for model in models:
            print(f"  - {model}")
    else:
        print("Models:  None available")
        if node_count == 0:
            print("  No nodes are connected. Run 'contribute' to share your models.")


def format_uptime(seconds: int) -> str:
    """Format seconds into a human-readable uptime string."""
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes}m {seconds % 60}s"
    hours = minutes // 60
    return f"{hours}h {minutes % 60}m"


def main():
    server_url = get_server_url()
    check_status(server_url)


if __name__ == "__main__":
    main()
