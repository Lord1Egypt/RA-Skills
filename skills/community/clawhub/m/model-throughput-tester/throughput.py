#!/usr/bin/env python3
"""
Model Throughput Tester
Two modes:
  1. API Mode: Direct call to OpenAI-compatible API (requires Key)
  2. Auto Mode: Via openclaw infer model run (no Key required)
"""
import argparse, time, json, csv, sys, os, statistics, subprocess, re, random
from datetime import datetime

# Token estimation constants
TOKEN_RATIO_EN = 0.75   # English: 1 token ≈ 0.75 word
TOKEN_RATIO_ZH = 1.5     # Chinese: 1 token ≈ 1.5 chars

def estimate_tokens(text):
    """Estimate token count from text."""
    ascii_chars = sum(1 for c in text if ord(c) < 128)
    if ascii_chars / len(text) > 0.7:
        return len(text.split()) / TOKEN_RATIO_EN
    else:
        return len(text) / TOKEN_RATIO_ZH

def detect_lang(text):
    ascii_chars = sum(1 for c in text if ord(c) < 128)
    return "en" if ascii_chars / len(text) > 0.7 else "zh"

# ─── Auto Mode: openclaw infer model run ───

def get_current_model():
    """Read current model from openclaw.json."""
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    try:
        with open(config_path) as f:
            d = json.load(f)
        # 1. models.default
        model = d.get("models", {}).get("default", "")
        if model:
            return model
        # 2. agents.defaults.model.primary
        model = d.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "")
        if model:
            return model
        # 3. Find provider with auth profile
        providers = d.get("models", {}).get("providers", {})
        for name, p in providers.items():
            if p.get("baseUrl"):
                return f"{name}/default"
        return ""
    except:
        return ""

def get_model_from_provider(model_ref):
    """Extract model ID and provider from provider/model format."""
    parts = model_ref.split("/", 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return None, model_ref

def get_provider_baseurl(provider):
    """Read provider baseUrl from openclaw.json."""
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    try:
        with open(config_path) as f:
            d = json.load(f)
        providers = d.get("models", {}).get("providers", {})
        p = providers.get(provider, {})
        return p.get("baseUrl", "")
    except:
        return ""

def run_auto_test(model, iterations, max_tokens, test_prompt, timeout):
    """Run throughput test via openclaw infer model run."""
    results = []

    for i in range(iterations):
        cmd = [
            "openclaw", "infer", "model", "run",
            "--model", model,
            "--prompt", test_prompt
        ]

        status = "ok"
        error_msg = ""
        output_tokens = 0

        try:
            start = time.perf_counter()
            r = subprocess.run(
                cmd,
                capture_output=True, text=True, timeout=timeout
            )
            elapsed = time.perf_counter() - start

            if r.returncode != 0:
                status = "cli_error"
                error_msg = r.stderr.strip()[:200]
            else:
                try:
                    d = json.loads(r.stdout)
                    if d.get("ok") and d.get("outputs"):
                        text = d["outputs"][0].get("text", "")
                        output_tokens = estimate_tokens(text)
                        if not text:
                            status = "empty_response"
                    else:
                        status = "api_error"
                        error_msg = json.dumps(d, ensure_ascii=False)[:200]
                except json.JSONDecodeError:
                    status = "json_error"
                    error_msg = r.stdout[:200]
        except subprocess.TimeoutExpired:
            elapsed = timeout
            status = "timeout"
            error_msg = f"timeout ({timeout}s)"
        except Exception as e:
            elapsed = 0
            status = "error"
            error_msg = str(e)
            elapsed = time.perf_counter() - start if 'start' in dir() else 0

        tokens_per_sec = round(output_tokens / elapsed, 2) if elapsed > 0 else 0
        results.append({
            "model": model,
            "elapsed": round(elapsed, 3),
            "output_tokens": round(output_tokens, 1),
            "tokens_per_sec": tokens_per_sec,
            "status": status,
            "error": error_msg,
            "iter": i + 1
        })

    return results

# ─── API Mode: Direct OpenAI-compatible API call ───

def parse_models(models_str):
    try:
        return json.loads(models_str)
    except json.JSONDecodeError:
        return [m.strip() for m in models_str.split(",")]

def call_model(url, key, model, system_prompt, test_prompt, max_tokens, timeout, stream, iter_num):
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    test_prompt_with_suffix = f"{test_prompt}\n[iteration:{iter_num} seed:{random.randint(10000,99999)}]"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": test_prompt_with_suffix}
        ],
        "max_tokens": max_tokens,
        "stream": stream
    }
    req_url = url.rstrip("/")
    if "/chat/completions" in req_url:
        pass
    elif req_url.endswith("/v1") or req_url.endswith("/v1/"):
        req_url += "/chat/completions"
    elif req_url.endswith("/v4") or req_url.endswith("/v4/"):
        req_url += "/chat/completions"
    else:
        req_url += "/v1/chat/completions"

    import urllib.request, urllib.error
    req = urllib.request.Request(
        req_url,
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST"
    )
    t0 = time.perf_counter()
    output_tokens = 0
    status = "ok"
    error_msg = ""
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            elapsed = time.perf_counter() - t0
            data = json.loads(body)
            usage = data.get("usage", {})
            output_tokens = usage.get("completion_tokens", 0)
            cached = usage.get("prompt_tokens_details", {}).get("cached_tokens", 0)
            if cached > 0:
                status = "cache_hit"
            if output_tokens == 0:
                msg = data["choices"][0]["message"]
                content = msg.get("content", "") or ""
                reasoning = msg.get("reasoning_content", "") or ""
                output_tokens = len(content) + len(reasoning)
    except urllib.error.HTTPError as e:
        elapsed = time.perf_counter() - t0
        try:
            err_body = json.loads(e.read())
            error_msg = err_body.get("error", {}).get("message", str(e))
        except:
            error_msg = str(e)
        status = f"http_{e.code}"
    except Exception as e:
        elapsed = time.perf_counter() - t0
        error_msg = str(e)
        status = "error"

    tokens_per_sec = round(output_tokens / elapsed, 2) if elapsed > 0 else 0
    return {
        "model": model,
        "elapsed": round(elapsed, 3),
        "output_tokens": output_tokens,
        "tokens_per_sec": tokens_per_sec,
        "status": status,
        "error": error_msg
    }

def build_markdown_report(results, mode, api_url, iterations, test_prompt, token_note=""):
    lines = [
        "# Model Throughput Report",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Mode:** {'Auto (openclaw infer)' if mode == 'auto' else 'API'}",
    ]
    if api_url:
        lines.append(f"**API URL:** {api_url}")
    lines.extend([
        f"**Iterations:** {iterations}",
        f"**Test Prompt:** {test_prompt}",
    ])
    if token_note:
        lines.append(f"**Token Note:** {token_note}")

    lines.extend([
        "",
        "## Summary",
        "| Model | Avg Tokens/s | Avg Latency(s) | Avg Output Tokens | Error Rate |",
        "|-------|-------------|----------------|-------------------|------------|",
    ])

    # results can be dict{model: [runs]} or [runs]
    if isinstance(results, dict):
        for model, runs in results.items():
            ok = [r for r in runs if r["status"] in ("ok", "cache_hit")]
            err = len(runs) - len(ok)
            if ok:
                avg_tps = statistics.mean(r["tokens_per_sec"] for r in ok)
                avg_lat = statistics.mean(r["elapsed"] for r in ok)
                avg_tok = statistics.mean(r["output_tokens"] for r in ok)
            else:
                avg_tps = avg_lat = avg_tok = 0
            err_rate = round(err / len(runs) * 100, 1) if runs else 0
            lines.append(f"| {model} | {avg_tps:.1f} | {avg_lat:.3f} | {avg_tok:.1f} | {err_rate}% |")
    else:
        ok = [r for r in results if r["status"] in ("ok", "cache_hit")]
        err = len(results) - len(ok)
        model = results[0]["model"] if results else "unknown"
        if ok:
            avg_tps = statistics.mean(r["tokens_per_sec"] for r in ok)
            avg_lat = statistics.mean(r["elapsed"] for r in ok)
            avg_tok = statistics.mean(r["output_tokens"] for r in ok)
        else:
            avg_tps = avg_lat = avg_tok = 0
        err_rate = round(err / len(results) * 100, 1) if results else 0
        lines.append(f"| {model} | {avg_tps:.1f} | {avg_lat:.3f} | {avg_tok:.1f} | {err_rate}% |")

    lines.extend(["", "## Detail", ""])
    all_runs = {}
    if isinstance(results, dict):
        all_runs = results
    else:
        for r in results:
            m = r["model"]
            all_runs.setdefault(m, []).append(r)

    for model, runs in all_runs.items():
        lines.append(f"### {model}")
        lines.append("| Iter | Latency(s) | Output Tokens | Tokens/s | Status |")
        lines.append("|------|------------|--------------|---------|--------|")
        for r in runs:
            status_icon = "✅" if r["status"] in ("ok", "cache_hit") else f"❌ {r['status']}"
            lines.append(f"| {r['iter']} | {r['elapsed']:.3f} | {r['output_tokens']:.0f} | {r['tokens_per_sec']:.1f} | {status_icon} |")
        lines.append("")

    return "\n".join(lines)

def write_csv(results, csv_path):
    rows = []
    if isinstance(results, dict):
        for model, runs in results.items():
            rows.extend(runs)
    else:
        rows = results
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "iter", "elapsed_s", "output_tokens", "tokens_per_s", "status", "error"])
        for r in rows:
            w.writerow([r["model"], r["iter"], r["elapsed"], round(r["output_tokens"]),
                       r["tokens_per_sec"], r["status"], r.get("error", "")])

def main():
    p = argparse.ArgumentParser(description="Model Throughput Tester — Auto (no key) or API mode")
    # Auto mode args
    p.add_argument("--auto", action="store_true", help="Auto mode: test current model via openclaw infer (no key needed)")
    p.add_argument("--model", default="", help="Model to test in auto mode (auto-detected if omitted)")
    # API mode args
    p.add_argument("--url", default="", help="API base URL (not needed for auto mode)")
    p.add_argument("--key", default="", help="API Key (not needed for auto mode)")
    p.add_argument("--models", default="", help="Comma-separated model list or JSON array (not needed for auto mode)")
    p.add_argument("--iterations", type=int, default=3, help="Test iterations per model (default 3)")
    p.add_argument("--max-tokens", type=int, default=512, help="Max output tokens (default 512)")
    p.add_argument("--system-prompt", default="You are a helpful assistant.", help="System prompt (API mode)")
    p.add_argument("--test-prompt", default="Write a detailed essay about summer meadows. No headings, no paragraph breaks, continuous prose only.", help="Test prompt")
    p.add_argument("--timeout", type=int, default=60, help="Request timeout in seconds (default 60)")
    p.add_argument("--stream", action="store_true", help="Use streaming mode (API mode)")
    p.add_argument("--output", default="throughput-report.md", help="Output report filename")
    p.add_argument("--csv", action="store_true", help="Also generate CSV report")

    args = p.parse_args()

    # ─── Auto Mode ───
    if args.auto:
        model = args.model or get_current_model()
        if not model:
            print("FAILED to detect current model, please use --model to specify one", file=sys.stderr)
            sys.exit(1)

        provider, model_id = get_model_from_provider(model)
        base_url = get_provider_baseurl(provider) if provider else ""
        display_model = model
        print(f"Auto mode: testing {display_model}", end="")
        if base_url:
            print(f" ({base_url})", end="")
        print(f", {args.iterations} iterations...\n")

        runs = run_auto_test(model, args.iterations, args.max_tokens, args.test_prompt, args.timeout)

        ok_count = sum(1 for r in runs if r["status"] == "ok")
        for r in runs:
            icon = "✅" if r["status"] == "ok" else f"❌({r['status']})"
            print(f"  {icon}")

        token_note = "Estimated (EN ~0.75 word/token, ZH ~1.5 chars/token)"
        report = build_markdown_report(runs, "auto", base_url, args.iterations, args.test_prompt, token_note)
        print("\n" + report)

        with open(args.output, "w") as f:
            f.write(report + "\n")
        print(f"\nReport saved: {os.path.abspath(args.output)}")

        if args.csv:
            csv_path = args.output.replace(".md", ".csv")
            write_csv(runs, csv_path)
            print(f"CSV saved: {os.path.abspath(csv_path)}")

        ok_runs = [r for r in runs if r["status"] == "ok"]
        if ok_runs:
            avg_tps = statistics.mean(r["tokens_per_sec"] for r in ok_runs)
            avg_tok = statistics.mean(r["output_tokens"] for r in ok_runs)
            print(f"\n{avg_tps:.1f} tokens/s avg ({avg_tok:.0f} tokens/req) for {display_model}")
        return

    # ─── API Mode ───
    if not args.url or not args.key or not args.models:
        print("API mode requires --url, --key, --models (or use --auto for no-key mode)", file=sys.stderr)
        print("Hint: --auto auto-tests current model with no configuration needed", file=sys.stderr)
        sys.exit(1)

    models = parse_models(args.models)
    results = {}

    print(f"Testing {len(models)} models, {args.iterations} iterations each...\n")

    for model in models:
        print(f"  {model}...", end=" ", flush=True)
        results[model] = []
        for i in range(args.iterations):
            r = call_model(args.url, args.key, model, args.system_prompt,
                          args.test_prompt, args.max_tokens, args.timeout, args.stream, i)
            r["iter"] = i + 1
            results[model].append(r)
            if r["status"] in ("ok", "cache_hit"):
                print("✅", end="", flush=True)
            else:
                print(f"❌({r['status']})", end="", flush=True)
        print()

    report = build_markdown_report(results, "api", args.url, args.iterations, args.test_prompt)
    print("\n" + report)

    with open(args.output, "w") as f:
        f.write(report + "\n")
    print(f"\nReport saved: {os.path.abspath(args.output)}")

    if args.csv:
        csv_path = args.output.replace(".md", ".csv")
        write_csv(results, csv_path)
        print(f"CSV saved: {os.path.abspath(csv_path)}")

if __name__ == "__main__":
    main()