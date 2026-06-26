import argparse
import json

from client import MumuClient


def build_status_summary(payload):
    total = payload.get("total") or 0
    completed = payload.get("completed") or 0
    current_chapter_number = payload.get("current_chapter_number")
    status = payload.get("status") or "unknown"
    error_message = payload.get("error_message")

    parts = [f"Batch {payload.get('batch_id')}: status={status}", f"progress={completed}/{total}"]
    if current_chapter_number:
        parts.append(f"current chapter {current_chapter_number}")
    if error_message:
        parts.append(f"error={error_message}")
    return " | ".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Check MuMu batch generation task status")
    parser.add_argument("--batch_id", required=True, type=str, help="Batch generation task ID")
    parser.add_argument("--project_id", type=str, help="The bound Novel Project ID (Optional, for consistency)")
    parser.add_argument("--style_id", type=str, help="The bound Style ID (Optional, overrides .env)")
    parser.add_argument("--json", action="store_true", help="Emit raw JSON")
    args = parser.parse_args()

    client = MumuClient(project_id=args.project_id, style_id=getattr(args, "style_id", None))
    try:
        payload = client.get(f"chapters/batch-generate/{args.batch_id}/status")
        if args.json:
            print(json.dumps(payload, ensure_ascii=False))
            return

        print(build_status_summary(payload))
        print(f"Retries: {payload.get('current_retry_count', 0)}/{payload.get('max_retries', 0)}")
        print(f"Failed chapters: {len(payload.get('failed_chapters') or [])}")
        print(f"Created at: {payload.get('created_at')}")
        print(f"Started at: {payload.get('started_at')}")
        print(f"Completed at: {payload.get('completed_at')}")
    except Exception as e:
        print(f"Failed to fetch batch status: {e}")


if __name__ == "__main__":
    main()
