#!/usr/bin/env python3
"""
Model Watch — Benchmark AI models and detect quality degradation.
Runs 7 standardized tests, tracks scores over time, fires alerts when models get dumber.

Usage:
  model-watch demo              # show benchmark questions
  model-watch submit '{"...":"..."}'  # submit model outputs
  model-watch history           # view score trend
  model-watch alert             # check for degradation
  model-watch serve             # show cron setup instructions

Source: Reddit pain #2 — AI models silently degrading
Repo: github.com/minirr890112-byte/HermesMade
"""

import json, os, time, sys
from datetime import datetime

DATA_FILE = os.path.expanduser("~/.hermes/model-watch-history.json")

BENCHMARKS = [
    {
        "id": "reasoning_1",
        "category": "reasoning",
        "prompt": "If a bat and ball cost $1.10 total, and the bat costs $1.00 more than the ball, how much does the ball cost? Show your reasoning step by step.",
        "expected_keywords": ["0.05", "5 cents", "$0.05"],
        "weight": 1.0,
    },
    {
        "id": "reasoning_2",
        "category": "reasoning",
        "prompt": "A farmer has 17 sheep. All but 9 die. How many are left?",
        "expected_keywords": ["9", "nine"],
        "weight": 0.5,
    },
    {
        "id": "coding_1",
        "category": "coding",
        "prompt": "Write a Python function that finds the first non-repeating character in a string. Include a test case. Return ONLY the code, no explanation.",
        "expected_keywords": ["def ", "return", "count", "OrderedDict", "Counter", "collections"],
        "weight": 1.5,
    },
    {
        "id": "coding_2",
        "category": "coding",
        "prompt": "What's wrong with this code? 'list = [1,2,3]; for i in list: list.append(i)' — explain in one sentence.",
        "expected_keywords": ["infinite", "loop", "forever", "never end", "grow"],
        "weight": 1.0,
    },
    {
        "id": "writing_1",
        "category": "writing",
        "prompt": "Write a 3-sentence product description for a smartphone. Make it compelling but factual. No buzzwords like 'revolutionary' or 'game-changing'.",
        "expected_keywords": [],
        "weight": 1.0,
    },
    {
        "id": "instruction_1",
        "category": "instruction_following",
        "prompt": "List 5 countries. Format them as a JSON array of strings. Output ONLY the JSON, nothing else.",
        "expected_keywords": ['["', '"]', '","'],
        "weight": 2.0,
    },
    {
        "id": "hallucination_1",
        "category": "hallucination",
        "prompt": "What is the capital of France? Answer with ONLY the city name, nothing else.",
        "expected_keywords": ["Paris"],
        "weight": 0.5,
    },
    {
        "id": "hallucination_2",
        "category": "hallucination",
        "prompt": "Who wrote the novel '1984'? Answer with ONLY the author's full name.",
        "expected_keywords": ["George Orwell"],
        "weight": 0.5,
    },
]


def load_history() -> list:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return []


def save_history(history: list):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(history, f, indent=2)


def score_response(benchmark: dict, response: str) -> float:
    response_lower = response.lower()
    score = 0.0
    max_score = len(benchmark["expected_keywords"]) if benchmark["expected_keywords"] else 3
    if max_score == 0:
        max_score = 3

    for kw in benchmark["expected_keywords"]:
        if kw.lower() in response_lower:
            score += 1.0

    if len(response) < 10:
        score -= 1
    if len(response) > 50:
        score += 0.5

    return max(0, min(1.0, score / max_score)) * benchmark["weight"]


def run_benchmarks(model_outputs: dict = None) -> dict:
    if model_outputs is None:
        print("❌ Model outputs required. Usage:")
        print("  Run each benchmark through your AI API, then:")
        print("  model-watch submit '<json_outputs>'")
        print("  Use 'model-watch demo' to see benchmark questions first.")
        sys.exit(1)

    results = {}
    total_score = 0
    total_weight = sum(b["weight"] for b in BENCHMARKS)

    for b in BENCHMARKS:
        if b["id"] not in model_outputs:
            continue
        s = score_response(b, model_outputs[b["id"]])
        results[b["id"]] = {
            "category": b["category"],
            "score": round(s, 3),
            "weight": b["weight"],
        }
        total_score += s

    overall = round(total_score / total_weight * 100, 1) if total_weight > 0 else 0

    entry = {
        "timestamp": datetime.now().isoformat(),
        "overall_score": overall,
        "details": results,
    }

    history = load_history()
    history.append(entry)
    save_history(history)

    return entry


def show_history():
    history = load_history()
    if not history:
        print("📭 No data yet. Run 'model-watch submit' first.")
        return

    print("=" * 60)
    print("  Model Watch — Quality Trend")
    print("=" * 60)
    print(f"{'Timestamp':<22} {'Score':>6} {'Status':>10}")
    print("-" * 42)

    scores = []
    for i, entry in enumerate(history):
        ts = entry["timestamp"][:19].replace("T", " ")
        sc = entry["overall_score"]
        scores.append(sc)

        if i > 0:
            prev = history[i - 1]["overall_score"]
            diff = sc - prev
            if diff < -10:
                status = "🔴 DEGRADED"
            elif diff < -5:
                status = "🟡 Dropped"
            elif diff > 5:
                status = "🟢 Improved"
            else:
                status = "➡ Stable"
        else:
            status = "——"

        print(f"{ts:<22} {sc:>5.1f}% {status:>10}")

    print("-" * 42)
    if len(scores) >= 2:
        trend = scores[-1] - scores[-2]
        print(f"Latest change: {trend:+.1f}%")
        avg = sum(scores) / len(scores)
        print(f"Historical avg: {avg:.1f}%")
        print(f"Latest score: {scores[-1]:.1f}%")

    if len(scores) >= 3:
        recent_avg = sum(scores[-3:]) / 3
        older_avg = sum(scores[:-3]) / max(1, len(scores) - 3)
        drop = older_avg - recent_avg
        if drop > 10:
            print(f"\n⚠ WARNING: Recent 3 avg {drop:.1f}% below historical. Possible model degradation!")


def check_alert() -> dict:
    history = load_history()
    if len(history) < 3:
        return {"alert": False, "reason": "Insufficient data (need at least 3 runs)"}

    recent = [h["overall_score"] for h in history[-3:]]
    older = [h["overall_score"] for h in history[:-3]]

    recent_avg = sum(recent) / 3
    older_avg = sum(older) / max(1, len(older))
    drop = older_avg - recent_avg

    alerts = []
    if drop > 15:
        alerts.append(f"🔴 Severe: recent 3 avg {recent_avg:.1f}% vs historical {older_avg:.1f}% (-{drop:.1f}%)")
    elif drop > 10:
        alerts.append(f"🟡 Warning: recent 3 avg {recent_avg:.1f}% vs historical {older_avg:.1f}% (-{drop:.1f}%)")

    if recent_avg < 50:
        alerts.append(f"🔴 Absolute score critical: {recent_avg:.1f}%")

    return {
        "alert": len(alerts) > 0,
        "alerts": alerts,
        "recent_avg": recent_avg,
        "older_avg": older_avg,
        "drop": drop,
    }


def show_benchmarks():
    print("=" * 60)
    print("  Model Watch — Benchmark Questions")
    print("=" * 60)
    for b in BENCHMARKS:
        print(f"\n[{b['id']}] {b['category']} (weight:{b['weight']})")
        print(f"  {b['prompt'][:120]}...")
        if b["expected_keywords"]:
            print(f"  Expected keywords: {', '.join(b['expected_keywords'])}")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "run":
        print("📊 Model Watch — Run Benchmarks")
        print("=" * 40)
        print("This tool needs model outputs from your AI API.")
        print("")
        print("Step 1: View questions")
        print("  model-watch demo")
        print("")
        print("Step 2: Run each question through your model")
        print("Step 3: Submit results")
        print("  model-watch submit '{\"reasoning_1\": \"...\", \"coding_1\": \"...\"}'")
        print("")

    elif cmd == "demo" or cmd == "benchmarks":
        show_benchmarks()

    elif cmd == "submit":
        if len(sys.argv) < 3:
            print("Usage: model-watch submit '<json_outputs>'")
            sys.exit(1)
        outputs = json.loads(sys.argv[2])
        result = run_benchmarks(outputs)
        print(f"✅ Benchmark complete. Score: {result['overall_score']}%")
        print(f"   Data saved to {DATA_FILE}")

    elif cmd == "history":
        show_history()

    elif cmd == "alert":
        result = check_alert()
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif cmd == "serve":
        print("🔄 Model Watch — Scheduled Monitoring")
        print("Set up a cron job to run periodically:")
        print("  model-watch alert  # returns JSON with alert status")
        print("")
        print("Example cron (runs daily at 9 AM):")
        print("  hermes cronjob create --name model-watch \\")
        print("    --schedule '0 9 * * *' \\")
        print("    --prompt 'Run model-watch alert. If alert fires, notify me.'")

    else:
        print("Model Watch — AI Model Quality Monitor")
        print("")
        print("Commands:")
        print("  demo        Show benchmark questions")
        print("  run         Interactive benchmark guide")
        print("  submit JSON Submit model outputs for scoring")
        print("  history     View score trend")
        print("  alert       Check for degradation")
        print("  serve       Show cron setup instructions")


if __name__ == "__main__":
    main()
