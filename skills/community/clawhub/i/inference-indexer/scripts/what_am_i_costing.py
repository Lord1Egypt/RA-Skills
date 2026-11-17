#!/usr/bin/env python3
"""
What is my agent costing me? - Inference Indexer skill command.

Reads the model IDs the user's harness is configured with, calls the
InferenceIndexer API for each, and prints:
  - what the user pays at their current host (if known)
  - what the same model costs at the cheapest II-known host
  - the annual delta at the user's actual monthly token volume

Zero setup: no API key required for the public data (1,000 req/day).
Usage:
  python3 what_am_i_costing.py <model_id> [model_id ...]
      [--host <provider name>]      # where you currently call it (optional)
      [--in <tok/month>] [--out <tok/month>]  # volume, default 1M in / 0.3M out
      [--current-in x] [--current-out y]      # override price at current host
  python3 what_am_i_costing.py --demo          # run with example models
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request

API = "https://api.inferenceindexer.ai"
UA = "inference-indexer-skill/1.1 (what-am-i-costing)"

# II model_ids resolve most reliably as "<org>/<name>"; bare names often 404.
KNOWN_ALIASES = {
    # bare config name -> II model_id
    "gpt-oss-120b": "openai/gpt-oss-120b",
    "gpt-oss-20b": "openai/gpt-oss-20b",
    "l3-lunaris-8b": "sao10k/l3-lunaris-8b",
    "deepseek-v4-flash": "deepseek/deepseek-v4-flash",
    "qwen3.8-max": "qwen/qwen3.8-max",
}


def http_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode())


def resolve_model(model_id):
    """Try the given id, then alias map, then a search fallback."""
    candidates = [model_id]
    bare = model_id.split("/")[-1].lower()
    if bare in KNOWN_ALIASES:
        candidates.append(KNOWN_ALIASES[bare])
    for c in candidates:
        try:
            return http_json(f"{API}/v1/models/{urllib.parse.quote(c, safe='')}/endpoints"), c
        except Exception:
            continue
    # last resort: server-side search
    try:
        res = http_json(f"{API}/v1/models?search={urllib.parse.quote(bare)}&limit=5")
        items = res if isinstance(res, list) else res.get("models", res.get("results", []))
        if items:
            found = items[0].get("model_id") or items[0].get("id")
            if found:
                return http_json(f"{API}/v1/models/{urllib.parse.quote(found, safe='')}/endpoints"), found
    except Exception:
        pass
    return None, None


def fmt_usd(x):
    if x is None:
        return "?"
    if x >= 100:
        return f"${x:,.0f}"
    if x >= 1:
        return f"${x:.2f}"
    return f"${x:.4f}"


def analyse(model_id, current_host=None, m_in=1_000_000, m_out=300_000,
            cur_in=None, cur_out=None):
    data, resolved = resolve_model(model_id)
    if not data:
        return (f"  {model_id}: not found in InferenceIndexer (691 models, 73 providers).\n"
                f"    Try the org/name form, e.g. 'openai/gpt-oss-120b'.")
    eps = data["endpoints"] if isinstance(data, dict) else data
    if not eps:
        return f"  {model_id}: no endpoints priced yet."

    eps = sorted(eps, key=lambda e: e["blended_price_per_m"])
    cheap = eps[0]
    name = data.get("name", resolved) if isinstance(data, dict) else resolved

    lines = []
    lines.append(f"  {name} - {len(eps)} hosts priced, cheapest {cheap['provider']} "
                 f"at {fmt_usd(cheap['blended_price_per_m'])}/M blended")

    # user's current host price
    cur = None
    if cur_in is not None and cur_out is not None:
        cur = {"provider": current_host or "your config",
               "input_price_per_m": cur_in, "output_price_per_m": cur_out,
               "blended_price_per_m": 0.4 * cur_in + 0.6 * cur_out}
    elif current_host:
        cur = next((e for e in eps if e["provider"].lower() == current_host.lower()), None)
        if cur is None:
            lines.append(f"    host '{current_host}' not in II's price list; pass --current-in/--current-out "
                         f"to price it exactly (e.g. from your provider's billing page)")
    if cur:
        lines.append(f"    you pay: {fmt_usd(cur['blended_price_per_m'])}/M blended "
                     f"({cur['provider']}: {fmt_usd(cur['input_price_per_m'])} in / {fmt_usd(cur['output_price_per_m'])} out)")

    # cost at volume
    monthly_at_current = (cur["input_price_per_m"] * m_in + cur["output_price_per_m"] * m_out) / 1e6 if cur else None
    monthly_at_cheap = (cheap["input_price_per_m"] * m_in + cheap["output_price_per_m"] * m_out) / 1e6
    lines.append(f"    at {m_in/1e6:.1f}M in / {m_out/1e6:.1f}M out per month:")
    if monthly_at_current is not None:
        lines.append(f"      current host: {fmt_usd(monthly_at_current)}/mo  ({fmt_usd(monthly_at_current*12)}/yr)")
    lines.append(f"      cheapest host: {fmt_usd(monthly_at_cheap)}/mo  ({fmt_usd(monthly_at_cheap*12)}/yr)")
    if monthly_at_current is not None and monthly_at_current > monthly_at_cheap:
        save = monthly_at_current - monthly_at_cheap
        pct = 100 * save / monthly_at_current if monthly_at_current else 0
        lines.append(f"      saving: {fmt_usd(save)}/mo = {fmt_usd(save*12)}/yr ({pct:.0f}%) by switching to {cheap['provider']}")

    # top-3 alternatives
    lines.append("    all hosts (cheapest first):")
    for e in eps[:3]:
        lines.append(f"      {e['provider']:<14} {fmt_usd(e['blended_price_per_m'])}/M blended  "
                     f"({fmt_usd(e['input_price_per_m'])} in / {fmt_usd(e['output_price_per_m'])} out)")
    if len(eps) > 3:
        lines.append(f"      ... {len(eps)-3} more hosts, run with --all to list")
    lines.append(f"    receipts: https://www.inferenceindexer.ai/models")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="What is my agent costing me?")
    ap.add_argument("models", nargs="*", help="model id(s), org/name preferred")
    ap.add_argument("--host", help="provider you currently use for the model(s)")
    ap.add_argument("--in", dest="m_in", type=float, default=1_000_000, help="input tokens/month (default 1M)")
    ap.add_argument("--out", dest="m_out", type=float, default=300_000, help="output tokens/month (default 0.3M)")
    ap.add_argument("--current-in", type=float, help="your current input price $/M (if host not in II)")
    ap.add_argument("--current-out", type=float, help="your current output price $/M")
    ap.add_argument("--all", action="store_true", help="list every host, not just top-3")
    ap.add_argument("--demo", action="store_true", help="run with example models")
    args = ap.parse_args()

    models = args.models or (["openai/gpt-oss-120b", "deepseek/deepseek-v4-flash"] if args.demo else None)
    if not models:
        ap.print_help()
        sys.exit(1)

    print("What is your agent costing you? (Inference Indexer)")
    print(f"Volume: {args.m_in/1e6:.1f}M in / {args.m_out/1e6:.1f}M out per month\n")
    for m in models:
        print(analyse(m, args.host, args.m_in, args.m_out, args.current_in, args.current_out))
        print()


if __name__ == "__main__":
    main()
