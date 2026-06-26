import argparse
import time
from client import MumuClient

def get_batch_blocker(project, chapters):
    wizard_status = (project.get("wizard_status") or "").lower()
    wizard_step = int(project.get("wizard_step") or 0)
    if wizard_status != "completed" or wizard_step < 4:
        return (
            "Project initialization is not finished yet. "
            "Run `bind_project.py --action status` and `--action resume` until the project is ready."
        )
    if not chapters:
        return (
            "Project has no chapter slots yet. "
            "Outline generation alone is not enough. Run `materialize_outlines.py --project_id <Your ID>` "
            "to convert outlines into chapter slots before batch generation."
        )
    return None


def is_terminal_batch_status(payload):
    return (payload.get("status") or "").lower() in {"completed", "failed", "cancelled"}


def build_batch_wait_summary(payload):
    status = payload.get("status") or "unknown"
    completed = payload.get("completed") or 0
    total = payload.get("total") or 0
    current_chapter_number = payload.get("current_chapter_number")

    summary = f"Batch {payload.get('batch_id')}: status={status} | progress={completed}/{total}"
    if current_chapter_number:
        summary += f" | current chapter {current_chapter_number}"
    if payload.get("error_message"):
        summary += f" | error={payload['error_message']}"
    return summary


def build_wait_timeout_message(batch_id, timeout):
    return (
        f"Batch is still running after {timeout} seconds. "
        f"Run `check_batch_status.py --batch_id {batch_id}` to confirm the latest server-side status."
    )


def wait_for_batch_completion(client, batch_id, timeout, poll_interval):
    deadline = time.monotonic() + max(0, timeout)
    while True:
        payload = client.get(f"chapters/batch-generate/{batch_id}/status")
        print(build_batch_wait_summary(payload))
        if is_terminal_batch_status(payload):
            return payload
        if time.monotonic() >= deadline:
            print(build_wait_timeout_message(batch_id, timeout))
            return payload
        time.sleep(poll_interval)

def main():
    parser = argparse.ArgumentParser(description="Trigger Batch Generation")
    parser.add_argument("--count", type=int, default=1, help="Number of chapters to generate")
    parser.add_argument("--wait", action="store_true", help="Poll batch status until completion or timeout")
    parser.add_argument("--poll-interval", type=int, default=10, help="Seconds between batch status polls when using --wait")
    parser.add_argument("--timeout", type=int, default=600, help="Maximum seconds to wait when using --wait")
    
    parser.add_argument("--project_id", type=str, help="The bound Novel Project ID (Required if not in env)")
    parser.add_argument("--style_id", type=str, help="The bound Style ID (Optional, overrides .env)")
    args = parser.parse_args()
    client = MumuClient(project_id=args.project_id, style_id=getattr(args, 'style_id', None))
    if not client.project_id:
        print("Error: --project_id argument is required or must be set in .env")
        return
    
    print(f"Detecting start chapter for project {client.project_id}...")
    try:
        project_resp = client.get(f"projects/{client.project_id}")
        chapters_resp = client.get(f"chapters/project/{client.project_id}", params={"limit": 1000})
        items = chapters_resp.get("items", [])
        blocker = get_batch_blocker(project_resp, items)
        if blocker:
            print(f"❌ {blocker}")
            return
        start_num = None
        for ch in items:
            print(f"Checking Chapter {ch.get('chapter_number')}: Words={ch.get('word_count')}, Status={ch.get('status')}")
            if ch.get("word_count", 0) == 0 or ch.get("status") == "draft":
                start_num = ch.get("chapter_number")
                break
                
        if start_num is None:
            print("❌ No empty draft chapters found in this project. All existing chapters seem to be completed.")
            return
            
        print(f"✅ Found empty draft at Chapter {start_num}. Starting batch generation for {args.count} chapters...")
        
        data = {
            "start_chapter_number": start_num,
            "count": args.count,
            "enable_analysis": True
        }
        if getattr(client, "style_id", None):
            data["style_id"] = client.style_id
            
        resp = client.post(f"chapters/project/{client.project_id}/batch-generate", json_data=data)
        print("Batch generation started successfully:")
        print(resp)
        if args.wait:
            batch_id = resp.get("batch_id")
            if not batch_id:
                print("Batch started, but no batch_id was returned for polling.")
                return
            final_status = wait_for_batch_completion(
                client,
                batch_id=batch_id,
                timeout=args.timeout,
                poll_interval=args.poll_interval,
            )
            if (final_status.get("status") or "").lower() == "completed":
                print("Batch generation completed. You can run fetch_unaudited.py next.")
    except Exception as e:
        print(f"Failed to trigger batch generation: {e}")

if __name__ == "__main__":
    main()
