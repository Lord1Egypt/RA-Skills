"""Offline JSONL event replay. Event IDs deduplicate whole receipts, including chain events.

Usage: python replay.py events.jsonl --out output_directory
There is deliberately no --live switch, exchange SDK, URL argument, or credential loader.
"""
import argparse
import hashlib
import json
from pathlib import Path
from time import perf_counter_ns
from pm_predict.engine import PaperEngine

METHODS = {"open_window", "book", "price", "health", "step", "ack", "cancel_ack", "reconcile",
           "fill", "confirm", "settle", "chain_result"}


def replay(events):
    e, seen, durations, duplicate_count = PaperEngine(), {}, [], 0
    for event in events:
        if set(event) != {"event_id", "method", "args"} or event["method"] not in METHODS:
            raise ValueError("not a normalized B paper event")
        key = event["event_id"]
        canonical = json.dumps(event, sort_keys=True, ensure_ascii=False, allow_nan=False)
        if key in seen:
            if canonical != seen[key]:
                raise ValueError(f"conflicting event ID {key}")
            duplicate_count += 1
            continue
        seen[key] = canonical
        before = perf_counter_ns()
        getattr(e, event["method"])(**event["args"])
        durations.append(perf_counter_ns() - before)
    result = e.summary()
    result.update({"input_events": len(seen), "duplicates_ignored": duplicate_count,
                   "local_replay_handler_ns": durations,
                   "warning": "SYNTHETIC receipts / offline replay; not a strategy backtest or exchange latency test"})
    return e, result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("events", type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()
    raw = args.events.read_bytes()
    events = [json.loads(s) for s in raw.decode("utf-8-sig").splitlines() if s.strip()]
    engine, result = replay(events)
    args.out.mkdir(parents=True, exist_ok=True)
    result["input_sha256"] = hashlib.sha256(raw).hexdigest()
    (args.out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), "utf-8")
    (args.out / "journal.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in engine.journal), "utf-8")
    (args.out / "intents.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in engine.intents), "utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "local_replay_handler_ns"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
