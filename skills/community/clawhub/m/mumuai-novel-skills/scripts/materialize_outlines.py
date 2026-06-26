import argparse
import json

from client import MumuClient


def select_outlines_to_materialize(outlines, limit=None):
    pending = [outline for outline in outlines if not outline.get("has_chapters")]
    pending.sort(key=lambda item: item.get("order_index") or 0)
    if limit is not None:
        return pending[:limit]
    return pending


def build_batch_expand_payload(project_id, outline_ids, chapters_per_outline=3, expansion_strategy="balanced"):
    return {
        "project_id": project_id,
        "outline_ids": outline_ids,
        "chapters_per_outline": chapters_per_outline,
        "expansion_strategy": expansion_strategy,
        "auto_create_chapters": False,
    }


def parse_sse_result(resp):
    final_result = None
    try:
        for line in resp.iter_lines():
            if not line:
                continue
            decoded = line.decode("utf-8")
            if not decoded.startswith("data: "):
                continue
            try:
                payload = json.loads(decoded[6:])
            except json.JSONDecodeError:
                continue

            ptype = payload.get("type")
            content = payload.get("content") or payload.get("message")
            if ptype in {"loading", "preparing", "generating", "parsing", "saving", "warning"} and content:
                print(f"[Agent Status] {content}")
            elif ptype == "error":
                raise RuntimeError(content or "Unknown SSE error")
            elif ptype == "result":
                final_result = payload.get("data")
    finally:
        resp.close()
    return final_result


def create_chapters_from_expansion(client, expansion_results):
    total_created = 0
    for result in expansion_results:
        chapter_plans = result.get("chapter_plans") or []
        if not chapter_plans:
            continue
        created = client.post(
            f"outlines/{result['outline_id']}/create-chapters-from-plans",
            json_data={"chapter_plans": chapter_plans},
        )
        total_created += created.get("chapters_created", 0)
        print(
            f"Created {created.get('chapters_created', 0)} chapter slots from outline "
            f"{created.get('outline_title', result['outline_id'])}."
        )
    return total_created


def main():
    parser = argparse.ArgumentParser(
        description="Materialize outline records into chapter slots using MuMu's real outline expansion flow."
    )
    parser.add_argument("--project_id", type=str, help="The bound Novel Project ID (Required if not in env)")
    parser.add_argument("--style_id", type=str, help="The bound Style ID (Optional, overrides .env)")
    parser.add_argument("--chapters-per-outline", type=int, default=3, help="Target chapter count per outline")
    parser.add_argument("--limit", type=int, default=1, help="Maximum number of pending outlines to materialize this run")
    parser.add_argument(
        "--expansion-strategy",
        type=str,
        default="balanced",
        choices=["balanced", "climax", "detail"],
        help="Outline expansion strategy",
    )
    args = parser.parse_args()

    client = MumuClient(project_id=args.project_id, style_id=getattr(args, "style_id", None))
    if not client.project_id:
        print("Error: --project_id argument is required or must be set in .env")
        return

    try:
        outlines_resp = client.get(f"outlines/project/{client.project_id}")
        outlines = outlines_resp.get("items", [])
        pending_outlines = select_outlines_to_materialize(outlines, limit=args.limit)
        if not pending_outlines:
            print("No outlines need chapter materialization right now.")
            return

        outline_ids = [outline["id"] for outline in pending_outlines]
        print(
            f"Materializing {len(outline_ids)} outlines into chapter slots for project {client.project_id}..."
        )
        payload = build_batch_expand_payload(
            project_id=client.project_id,
            outline_ids=outline_ids,
            chapters_per_outline=args.chapters_per_outline,
            expansion_strategy=args.expansion_strategy,
        )
        resp = client.post("outlines/batch-expand-stream", json_data=payload, stream=True)
        expansion_result = parse_sse_result(resp)
        if not expansion_result:
            print("Expansion finished, but no result payload was captured.")
            return

        total_created = create_chapters_from_expansion(
            client,
            expansion_result.get("expansion_results", []),
        )
        print("\n=== OUTLINE MATERIALIZATION REPORT ===")
        print(f"Outlines processed: {expansion_result.get('total_outlines_expanded', 0)}")
        print(f"Chapter slots created: {total_created}")
        print("You can run trigger_batch.py next if empty draft chapters now exist.")
    except Exception as e:
        print(f"Failed to materialize outlines: {e}")


if __name__ == "__main__":
    main()
