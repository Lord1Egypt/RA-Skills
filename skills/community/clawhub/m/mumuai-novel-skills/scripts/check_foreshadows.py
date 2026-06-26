import argparse
from client import MumuClient


def render_empty_pending_message():
    return (
        "No pending foreshadows were returned from the `pending-resolve` view. "
        "This does not mean newly added foreshadows failed to save; it only means none are currently "
        "queued as unresolved hooks for the requested chapter context."
    )


def main():
    parser = argparse.ArgumentParser(description="Pulls recent RAG memories and unresolved foreshadowing")
    parser.add_argument("--action", choices=["list-pending"], default="list-pending", help="Action to perform")
    
    parser.add_argument("--project_id", type=str, help="The bound Novel Project ID (Required if not in env)")
    parser.add_argument("--style_id", type=str, help="The bound Style ID (Optional, overrides .env)")
    args = parser.parse_args()
    client = MumuClient(project_id=args.project_id, style_id=getattr(args, 'style_id', None))
    if not client.project_id:
        print("Error: --project_id argument is required or must be set in .env")
        return
    
    if args.action == "list-pending":
        print(f"Fetching unresolved plot hooks from the pending-resolve view for project {client.project_id}...")
        try:
            resp = client.get(f"foreshadows/projects/{client.project_id}/pending-resolve", params={"current_chapter": 1})
            items = resp if isinstance(resp, list) else resp.get("items", [])
            print("\n=== Unresolved Foreshadows ===")
            if not items:
                print(render_empty_pending_message())
            for f in items:
                print(f"- [ID: {f.get('id')}] Content: {f.get('content')} | Severity: {f.get('importance_score', 0)}")
            print("==============================")
            print("Instruction to Agent: Treat this as a pending-resolve queue, not as a full list of all stored foreshadows.")
        except Exception as e:
            print(f"Failed to fetch pending foreshadows: {e}")
            
if __name__ == "__main__":
    main()
