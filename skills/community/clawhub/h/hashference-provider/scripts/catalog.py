#!/usr/bin/env python3
"""Read public Hashference metadata and print to stdout; no file writes or credentials."""
import argparse
import json
import sys
import urllib.request
from pathlib import Path

URL = "https://hashference.com/v1/catalog"
ENDPOINTS = {"chat": "/v1/chat/completions", "responses": "/v1/responses", "messages": "/v1/messages"}
APIS = {"chat": "openai-completions", "responses": "openai-responses", "messages": "anthropic-messages"}


def rows_from(payload):
    rows = payload if isinstance(payload, list) else payload.get("data", payload.get("models")) if isinstance(payload, dict) else None
    if not isinstance(rows, list) or not rows:
        raise ValueError("Expected a nonempty catalog array or data/models array")
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
            raise ValueError("Catalog row requires a nonempty string id")
        if row["id"] in seen:
            raise ValueError("Duplicate catalog id: " + row["id"])
        seen.add(row["id"])
    return rows


def select(rows, transport="chat", aliases=False, agents_only=False, ids=None):
    selected = [r for r in rows if r.get("availability") == "live"
                and ENDPOINTS[transport] in r.get("endpoints", [])
                and (aliases or not r.get("same_model_as"))
                and (not agents_only or r.get("supports_tools") is True)]
    if ids:
        selected = [r for r in selected if r["id"] in ids]
        missing = set(ids) - {r["id"] for r in selected}
        if missing:
            raise ValueError("Not live/eligible for chosen filters: " + ", ".join(sorted(missing)))
    if not selected:
        raise ValueError("No models match; inspect catalog and transport/alias/tool filters")
    return selected


def positive(row, field):
    value = row.get(field)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(row["id"] + ": missing/invalid " + field)
    return value


def model_config(row, transport):
    context = positive(row, "context_length")
    hard_output = positive(row, "max_output_tokens")
    output = min(positive(row, "default_max_output_tokens"), hard_output)
    if "max_input_tokens" in row:
        context = min(context, positive(row, "max_input_tokens") + output)
    if output >= context:
        raise ValueError(row["id"] + ": output budget leaves no input space")
    result = {"id": row["id"], "name": row.get("name", row["id"]),
              "api": APIS[transport], "input": ["text"],
              "contextWindow": context, "maxTokens": output}
    cost = {}
    fields = {"input": "input", "output": "output", "cacheRead": "cached_input", "cacheWrite": "cache_write_input"}
    for target, source in fields.items():
        value = row.get("credits_per_million_" + source + "_tokens")
        if value is not None:
            if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
                raise ValueError(row["id"] + ": invalid price")
            cost[target] = value / 1000
    if cost:
        result["cost"] = cost
    return result


def render(rows, fmt, transport):
    if fmt == "openclaw":
        return json.dumps([model_config(r, transport) for r in rows], indent=2) + "\n"
    if fmt == "json":
        return json.dumps(rows, indent=2) + "\n"
    lines = ["# Hashference model catalog", "", "Snapshot only. Refresh before setup, pricing advice, or inference.",
             "Prices: USD per million tokens (catalog credits / 1,000). ? means unreported.", "",
             "| Model ID | Name | Tools | Context | Max input | Default / max output | Input / output USD | Hosting provider |",
             "| --- | --- | --- | ---: | ---: | ---: | --- | --- |"]
    def cell(v):
        return str(v).replace("|", "\\|").replace("\n", " ")
    def price(r, suffix):
        v = r.get("credits_per_million_" + suffix + "_tokens")
        return "?" if v is None else format(v / 1000, ".6g")
    for r in rows:
        vals = [r["id"], r.get("name", ""), r.get("supports_tools", "?"), r.get("context_length", "?"),
                r.get("max_input_tokens", "—"), str(r.get("default_max_output_tokens", "?")) + " / " + str(r.get("max_output_tokens", "?")),
                price(r, "input") + " / " + price(r, "output"), r.get("provider_name", "?")]
        lines.append("| " + " | ".join(cell(v) for v in vals) + " |")
    return "\n".join(lines) + "\n"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, help="Offline public catalog JSON; otherwise fetch live HTTPS")
    p.add_argument("--format", choices=["markdown", "json", "openclaw"], default="markdown")
    p.add_argument("--transport", choices=ENDPOINTS, default="chat")
    p.add_argument("--include-aliases", action="store_true", help="Include same_model_as protocol aliases")
    p.add_argument("--agents-only", action="store_true", help="Require advertised tool support")
    p.add_argument("--model", action="append", help="Exact catalog ID; repeat to choose several")
    args = p.parse_args(argv)
    try:
        if args.input:
            payload = json.loads(args.input.read_text())
        else:
            req = urllib.request.Request(URL, headers={"Accept": "application/json", "User-Agent": "hashference-openclaw-skill/1.0"})
            with urllib.request.urlopen(req, timeout=30) as response:
                payload = json.load(response)
        rows = select(rows_from(payload), args.transport, args.include_aliases, args.agents_only, args.model)
        output = render(rows, args.format, args.transport)
        sys.stdout.write(output)
        print(str(len(rows)) + " live catalog entries selected", file=sys.stderr)
    except (ValueError, OSError, TypeError, KeyError) as exc:
        p.exit(1, "Catalog error: " + str(exc) + "\n")


if __name__ == "__main__":
    main()
