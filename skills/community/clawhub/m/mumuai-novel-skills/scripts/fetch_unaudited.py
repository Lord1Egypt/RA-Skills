import argparse
from client import MumuClient


def is_review_candidate(item):
    status = (item.get("status") or "").lower()
    word_count = item.get("word_count") or 0
    return word_count > 0 and status in {"draft", "generated", "pending_review", "needs_review", "completed"}


def select_review_candidates(items):
    return [item for item in items if is_review_candidate(item)]


def build_review_summary(items):
    review_candidates = select_review_candidates(items)
    return (
        f"Retrieved {len(items)} chapters from the full chapter list. "
        f"Found {len(review_candidates)} review candidates with generated content."
    )


def render_chapter_line(item):
    return (
        f"- Chapter ID: {item['id']} | Title: {item['title']} | "
        f"Status: {item.get('status')} | Words: {item.get('word_count')}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="List project chapters and highlight likely review candidates."
    )
    parser.add_argument("--project_id", type=str, help="The bound Novel Project ID (Required if not in env)")
    parser.add_argument("--style_id", type=str, help="The bound Style ID (Optional, overrides .env)")
    args = parser.parse_args()
    client = MumuClient(project_id=args.project_id, style_id=getattr(args, 'style_id', None))
    if not client.project_id:
        print("Error: --project_id argument is required or must be set in .env")
        return
    
    print(f"Fetching chapter list for project {client.project_id}...")
    
    try:
        resp = client.get(f"chapters/project/{client.project_id}", params={"limit": 100})
        items = resp.get("items", [])
        review_candidates = select_review_candidates(items)

        print(build_review_summary(items))
        print("Note: this script reads the full chapter list endpoint, not a dedicated unaudited inbox.")
        
        if review_candidates:
            print("\nLikely review candidates:")
            for item in review_candidates:
                print(render_chapter_line(item))
                print(item.get('content', '')[:100] + "...\n")
        else:
            print("\nNo likely review candidates found right now.")

        if items:
            print("Full chapter list:")
            for item in items:
                print(render_chapter_line(item))
        else:
            print("No chapters found in this project.")
            
    except Exception as e:
        print(f"Failed to fetch chapters: {e}")

if __name__ == "__main__":
    main()
