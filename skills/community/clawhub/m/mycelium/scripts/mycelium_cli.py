import argparse
import json
import os
import sys
import httpx

# Path setup to import the local lib (Monorepo mode)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

try:
    from mycelium_sdk.client import MyceliumClient
except ImportError as e:
    print(json.dumps({"error": f"Failed to import SDK: {str(e)}"}))
    sys.exit(1)

def get_client():
    api_url = os.getenv("MYCELIUM_API_URL", "https://mycelium-platform.onrender.com").rstrip("/")
    api_key = os.getenv("MYCELIUM_API_KEY")
    
    if not api_key:
        print(json.dumps({
            "error": "Missing MYCELIUM_API_KEY. Please run the 'register' command or set it in your environment."
        }))
        sys.exit(1)
        
    return MyceliumClient(api_url=api_url, api_key=api_key)

def main():
    parser = argparse.ArgumentParser(prog="mycelium_cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # register
    reg_p = subparsers.add_parser("register")
    reg_p.add_argument("--handle", help="User handle (optional)")

    # seek
    seek_p = subparsers.add_parser("seek")
    seek_p.add_argument("--goal", required=True)
    seek_p.add_argument("--scope", choices=["task", "bug"], default="task")
    seek_p.add_argument("--tags", default="")

    # publish
    pub_p = subparsers.add_parser("publish")
    pub_p.add_argument("--goal", required=True)
    pub_p.add_argument("--scope", choices=["task", "bug"], default="task")
    pub_p.add_argument("--tags", default="")
    pub_p.add_argument("--path", required=True, help="JSON string of the path/steps")
    pub_p.add_argument("--confirmed", action="store_true", help="Flag to indicate user has confirmed the data")

    # feedback
    fb_p = subparsers.add_parser("feedback")
    fb_p.add_argument("--id", required=True)
    fb_p.add_argument("--result", choices=["success", "fail", "unknown"], required=True)

    args = parser.parse_args()

    try:
        api_url = os.getenv("MYCELIUM_API_URL", "https://mycelium-platform.onrender.com").rstrip("/")

        if args.command == "register":
            resp = httpx.post(f"{api_url}/users/register", json={"handle": args.handle}, timeout=10.0)
            resp.raise_for_status()
            print(json.dumps(resp.json(), indent=2))
            return

        client = get_client()

        if args.command == "seek":
            tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
            res = client.seek(goal=args.goal, scope=args.scope, tags=tags)
            print(json.dumps(res, indent=2, ensure_ascii=False))

        elif args.command == "publish":
            tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
            path_obj = json.loads(args.path)
            
            if not args.confirmed:
                print(json.dumps({
                    "action": "confirm_required",
                    "type": "pheromone_publication",
                    "message": "⚠️ CONFIRMATION: Review this strategic path before publishing.",
                    "data": {
                        "goal": args.goal,
                        "tags": tags,
                        "path_to_publish": path_obj
                    }
                }, indent=2, ensure_ascii=False))
                sys.exit(0)

            # In the CLI, we call with confirmed=True
            ph_id = client.publish(goal=args.goal, scope=args.scope, tags=tags, path=path_obj, confirmed=True)
            print(json.dumps({"status": "published", "id": ph_id}))

        elif args.command == "feedback":
            res = client.feedback(pheromone_id=args.id, result=args.result)
            print(json.dumps(res, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
