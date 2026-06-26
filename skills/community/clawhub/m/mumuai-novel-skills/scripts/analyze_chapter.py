import time
import argparse
from client import MumuClient


def extract_report_fields(payload):
    analysis = payload.get("analysis") if isinstance(payload, dict) else None
    source = analysis if isinstance(analysis, dict) else payload
    return {
        "overall_quality_score": source.get("overall_quality_score"),
        "coherence_score": source.get("coherence_score"),
        "engagement_score": source.get("engagement_score"),
        "pacing_score": source.get("pacing_score"),
        "analysis_report": source.get("analysis_report") or source.get("comprehensive_review"),
        "suggestions": source.get("suggestions") or [],
        "hooks": source.get("hooks") or [],
        "foreshadows": source.get("foreshadows") or [],
    }


def build_score_summary(report):
    return (
        f"Scores: Overall({report.get('overall_quality_score')}) | "
        f"Coherence({report.get('coherence_score')}) | "
        f"Engagement({report.get('engagement_score')}) | "
        f"Pacing({report.get('pacing_score')})"
    )


def main():
    parser = argparse.ArgumentParser(description="Trigger System RAG Analysis for a chapter")
    parser.add_argument("--chapter_id", required=True, help="Chapter ID to analyze")
    parser.add_argument("--timeout", type=int, default=300, help="Maximum seconds to wait for analysis completion")
    parser.add_argument("--interval", type=int, default=3, help="Polling interval in seconds")
    
    parser.add_argument("--project_id", type=str, help="The bound Novel Project ID (Required if not in env)")
    parser.add_argument("--style_id", type=str, help="The bound Style ID (Optional, overrides .env)")
    args = parser.parse_args()
    client = MumuClient(project_id=args.project_id, style_id=getattr(args, 'style_id', None))
    if not client.project_id:
        print("Error: --project_id argument is required or must be set in .env")
        return
    
    print(f"Triggering RAG analysis for chapter {args.chapter_id} in project {client.project_id}...")
    
    try:
        # Trigger Analysis
        client.post(f"chapters/{args.chapter_id}/analyze")
        
        # Poll for completion
        print("Waiting for RAG analysis to complete...")
        deadline = time.monotonic() + args.timeout
        while True:
            status_resp = client.get(f"chapters/{args.chapter_id}/analysis/status")
            status = status_resp.get("status")
            if status in ["completed", "failed", "none"]:
                break
            if time.monotonic() >= deadline:
                print(f"Analysis timed out after {args.timeout} seconds. Last known status: {status}")
                return
            time.sleep(args.interval)
            
        # Fetch the actual report
        report_resp = client.get(f"chapters/{args.chapter_id}/analysis")
        report = extract_report_fields(report_resp)
        print("\n=== SYSTEM RAG ANALYSIS REPORT ===")
        print(build_score_summary(report))
        print(report.get('analysis_report') or 'No comprehensive review returned.')
        if report.get("suggestions"):
            print("\nSuggestions:")
            for item in report["suggestions"]:
                print(f"- {item}")
        if report.get("hooks"):
            print(f"\nHooks detected: {len(report['hooks'])}")
        if report.get("foreshadows"):
            print(f"Foreshadows detected: {len(report['foreshadows'])}")
        print("==================================")
        print("Note: If the report shows inconsistencies or missing plot goals, use review_chapter.py --action rewrite")
    except Exception as e:
        print(f"Analysis failed: {e}")

if __name__ == "__main__":
    main()
