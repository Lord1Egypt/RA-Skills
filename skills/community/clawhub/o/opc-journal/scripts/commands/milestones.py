"""Journal command: milestones (candidate extraction for LLM validation)."""
from scripts.commands._meta import get_language


def run(customer_id: str, args: dict) -> dict:
    """Store a milestone candidate. Interpretation and classification are left to the caller (LLM)."""
    content = args.get("content", "")
    day = args.get("day", 1)
    lang = get_language(customer_id)

    if not content:
        return {"status": "error", "result": None, "message": "content is required"}

    # No hardcoded keyword matching. Return the raw candidate for the caller to judge.
    candidate = {
        "customer_id": customer_id,
        "day": day,
        "language": lang,
        "raw_content": content.strip(),
        "candidate_type": "milestone",
    }

    return {
        "status": "success",
        "result": {
            "customer_id": customer_id,
            "day": day,
            "language": lang,
            "candidate": candidate,
            "note": "Content stored as milestone candidate. Classification should be performed by the caller.",
        },
        "message": f"Milestone candidate recorded for {customer_id}",
    }
