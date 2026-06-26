import argparse
from client import MumuClient

def build_foreshadow_title(content: str) -> str:
    cleaned = " ".join(content.strip().split())
    if not cleaned:
        return "手动伏笔"
    return cleaned[:60]


def build_add_foreshadow_success_message() -> str:
    return (
        "Foreshadow added successfully. "
        "Note: newly added foreshadows may not appear immediately in `check_foreshadows.py` because that script reads the "
        "`pending-resolve` queue rather than the full stored foreshadow set."
    )

def main():
    parser = argparse.ArgumentParser(description="Manage RAG Memory and Foreshadows")
    parser.add_argument("--action", required=True, choices=["add_foreshadow"], help="Action to perform")
    parser.add_argument("--content", required=True, help="Content of the foreshadow")
    
    parser.add_argument("--project_id", type=str, help="The bound Novel Project ID (Required if not in env)")
    parser.add_argument("--style_id", type=str, help="The bound Style ID (Optional, overrides .env)")
    args = parser.parse_args()
    client = MumuClient(project_id=args.project_id, style_id=getattr(args, 'style_id', None))
    if not client.project_id:
        print("Error: --project_id argument is required or must be set in .env")
        return
    
    print(f"Executing {args.action} on bound project {client.project_id}...")
    
    try:
        if args.action == "add_foreshadow":
            data = {
                "project_id": client.project_id,
                "title": build_foreshadow_title(args.content),
                "content": args.content,
                "status": "pending",
            }
            client.post("foreshadows", json_data=data)
            print(build_add_foreshadow_success_message())
            
    except Exception as e:
        print(f"Memory management failed: {e}")

if __name__ == "__main__":
    main()
