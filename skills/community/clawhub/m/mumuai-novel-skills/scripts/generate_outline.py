import json
import argparse
from client import MumuClient


def extract_error_message(payload):
    return (
        payload.get("content")
        or payload.get("message")
        or payload.get("detail")
        or payload.get("error")
        or "Unknown outline generation error"
    )


def main():
    parser = argparse.ArgumentParser(description="Trigger AI Outline Generation")
    parser.add_argument("--count", type=int, default=5, help="Number of chapters to outline")
    parser.add_argument("--mode", type=str, default="auto", choices=["auto", "new", "continue"])
    
    parser.add_argument("--project_id", type=str, help="The bound Novel Project ID (Required if not in env)")
    parser.add_argument("--style_id", type=str, help="The bound Style ID (Optional, overrides .env)")
    args = parser.parse_args()
    client = MumuClient(project_id=args.project_id, style_id=getattr(args, 'style_id', None))
    if not client.project_id:
        print("Error: --project_id argument is required or must be set in .env")
        return
    
    print(f"Triggering outline generation ({args.mode}) for {args.count} chapters on project {client.project_id}...")
    try:
        data = {
            "project_id": client.project_id,
            "chapter_count": args.count,
            "mode": args.mode
        }
        resp = client.post("outlines/generate-stream", json_data=data, stream=True)
        print("Waiting for outline generation to complete (this may take a few minutes)...")
        
        final_result = None
        try:
            for line in resp.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    if decoded.startswith("data: "):
                        try:
                            payload = json.loads(decoded[6:])
                            if payload.get("type") == "parsing":
                                print(f"[Agent Status] {payload.get('content')}")
                            elif payload.get("type") == "saving":
                                print(f"[Agent Status] {payload.get('content')}")
                            elif payload.get("type") == "error":
                                print(f"❌ Error: {extract_error_message(payload)}")
                                return
                            elif payload.get("type") == "result":
                                final_result = payload.get("data")
                        except json.JSONDecodeError:
                            pass
        finally:
            resp.close()
                        
        print("\n=== OUTLINE GENERATION REPORT ===")
        if final_result:
            print(f"Total new chapters outlined: {final_result.get('new_chapters', 0)}")
            print(f"Message: {final_result.get('message', '')}")
            print("Successfully expanded the novel's creative runway.")
            print("If the project still has no chapter slots, run materialize_outlines.py next before trigger_batch.py.")
        else:
            print("Completed, but no final result payload was captured. Please check the MuMu console.")
            
    except Exception as e:
        print(f"Failed to generate outline: {e}")

if __name__ == "__main__":
    main()
