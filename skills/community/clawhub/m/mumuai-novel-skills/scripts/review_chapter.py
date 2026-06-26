import argparse
import os
import sys
from client import MumuClient

def read_rewrite_content(args):
    if args.content is not None:
        return args.content

    if args.file:
        if not os.path.exists(args.file):
            raise FileNotFoundError(args.file)
        with open(args.file, "r", encoding="utf-8") as f:
            return f.read()

    if not sys.stdin.isatty():
        return sys.stdin.read()

    return None

def main():
    parser = argparse.ArgumentParser(description="Audit/Approve/Rewrite a generated chapter")
    parser.add_argument("--action", choices=["approve", "rewrite"], required=True, help="Action to perform")
    parser.add_argument("--chapter_id", type=str, required=True, help="The Chapter ID to act upon")
    parser.add_argument("--file", type=str, help="Path to a text file containing the rewritten content (for rewrite action)")
    parser.add_argument("--content", type=str, help="Raw rewritten chapter content (preferred for agent platforms)")
    
    parser.add_argument("--project_id", type=str, help="The bound Novel Project ID (Required if not in env)")
    parser.add_argument("--style_id", type=str, help="The bound Style ID (Optional, overrides .env)")
    args = parser.parse_args()
    client = MumuClient(project_id=args.project_id, style_id=getattr(args, 'style_id', None))
    if not client.project_id:
        print("Error: --project_id argument is required or must be set in .env")
        return
    
    if args.action == "approve":
        print(f"Approving chapter {args.chapter_id}...")
        try:
            client.put(f"chapters/{args.chapter_id}", json_data={"status": "published"})
            print("✅ Chapter is now PUBLISHED and will be hidden from the unaudited inbox.")
        except Exception as e:
            print(f"Failed to approve chapter: {e}")
            
    elif args.action == "rewrite":
        try:
            new_text = read_rewrite_content(args)
        except FileNotFoundError:
            print("❌ Error: --file must point to a valid text file containing the new chapter text.")
            return

        if not new_text:
            print("❌ Error: provide rewrite text via --content, --file, or stdin.")
            return
            
        print(f"Submitting heavily edited rewrite for chapter {args.chapter_id} (Words: {len(new_text)})...")
        try:
            client.put(f"chapters/{args.chapter_id}", json_data={"content": new_text, "status": "published"})
            print("✅ Chapter successfully overwritten and PUBLISHED!")
        except Exception as e:
            print(f"Failed to rewrite chapter: {e}")

if __name__ == "__main__":
    main()
