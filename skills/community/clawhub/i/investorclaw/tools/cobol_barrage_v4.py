# SPDX-License-Identifier: Apache-2.0
"""v4.0 cobol barrage runner.

Hits the ic-engine MCP-HTTP endpoint at :8090/mcp directly (no agent
runtime in the loop) with the canonical 30-prompt cobol set, N=3 trials.

Also runs a small parallel multi-stream pass to validate concurrent
session behavior — multiple agents pointing at the same engine.

Output:
  reports/v4-barrage-<ts>/sequential.jsonl    one line per (prompt, trial)
  reports/v4-barrage-<ts>/parallel.jsonl      multi-stream results
  reports/v4-barrage-<ts>/summary.md          score + perf + failure list
"""
from __future__ import annotations

import argparse
import asyncio
import datetime
import json
import os
import re
import sys
import time
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import httpx


# ── config ──────────────────────────────────────────────────────────


DEFAULT_BASE = os.environ.get("IC_MCP_BASE", "http://127.0.0.1:8090")
DEFAULT_PROMPTS = "/tmp/nlq-prompts.json"
DEFAULT_TIMEOUT = 240.0   # 240s absorbs ic-engine v2.5.x cold-cache (~45-90s) + margin for retries
DEFAULT_TRIALS = 3
PARALLEL_STREAMS = 4
PARALLEL_PROMPTS = ["p01-holdings-1", "p03-performance-1", "p06-news-holdings-1", "p15-bonds-1"]


# ── MCP client ──────────────────────────────────────────────────────


@dataclass
class TrialResult:
    prompt_id: str
    prompt_text: str
    trial: int
    exit_code: int | None
    duration_ms: int | None
    wallclock_ms: int
    has_ic_result: bool
    has_hmac: bool
    narrative_chars: int
    is_error: bool
    error_message: str | None


class McpClient:
    """Minimal streamable-HTTP MCP client for portfolio_ask testing."""

    def __init__(self, base: str, client_name: str = "barrage") -> None:
        self.base = base.rstrip("/")
        self.client_name = client_name
        self.session_id: str | None = None
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(DEFAULT_TIMEOUT, connect=10.0),
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
            },
        )

    async def initialize(self) -> None:
        body = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": self.client_name, "version": "0.1"},
            },
        }
        r = await self.client.post(f"{self.base}/mcp", json=body)
        r.raise_for_status()
        self.session_id = r.headers.get("mcp-session-id")
        if not self.session_id:
            raise RuntimeError("no mcp-session-id returned from initialize")
        # send initialized notification
        await self.client.post(
            f"{self.base}/mcp",
            json={"jsonrpc": "2.0", "method": "notifications/initialized"},
            headers={"mcp-session-id": self.session_id},
        )

    async def call_portfolio_ask(self, question: str) -> dict[str, Any]:
        body = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "tools/call",
            "params": {"name": "portfolio_ask", "arguments": {"question": question}},
        }
        headers = {"mcp-session-id": self.session_id} if self.session_id else {}
        r = await self.client.post(f"{self.base}/mcp", json=body, headers=headers)
        r.raise_for_status()
        # SSE event stream — last "data:" line is the JSON-RPC response
        text = r.text
        last_data = None
        for m in re.finditer(r"^data: (.+)$", text, re.MULTILINE):
            last_data = m.group(1)
        if last_data is None:
            raise RuntimeError(f"no data line in MCP response (head: {text[:200]!r})")
        return json.loads(last_data)

    async def aclose(self) -> None:
        await self.client.aclose()


# ── helpers ─────────────────────────────────────────────────────────


def parse_response(rpc: dict[str, Any]) -> tuple[dict[str, Any], str, bool]:
    """Returns (structured, narrative, is_error)."""
    result = rpc.get("result", {})
    structured = result.get("structuredContent", {}) or {}
    narrative = structured.get("narrative", "") or ""
    is_error = bool(result.get("isError", False))
    return structured, narrative, is_error


def score_trial(struct: dict[str, Any], narrative: str, is_error: bool) -> TrialResult:
    """Build a TrialResult; caller fills in prompt + trial + wallclock."""
    exit_code = struct.get("exit_code")
    duration_ms = struct.get("duration_ms")
    ic = struct.get("ic_result") or {}
    inner = ic.get("ic_result") if isinstance(ic, dict) else None
    has_ic = bool(inner) if inner is not None else bool(ic)
    has_hmac = "hmac" in (inner or ic or {}) if isinstance(ic, dict) else False
    return TrialResult(
        prompt_id="",
        prompt_text="",
        trial=-1,
        exit_code=exit_code if isinstance(exit_code, int) else None,
        duration_ms=duration_ms if isinstance(duration_ms, int) else None,
        wallclock_ms=0,
        has_ic_result=has_ic,
        has_hmac=has_hmac,
        narrative_chars=len(narrative),
        is_error=is_error,
        error_message=None,
    )


# ── sequential barrage ──────────────────────────────────────────────


async def run_sequential(
    base: str,
    prompts: list[dict[str, Any]],
    trials: int,
    out: Path,
) -> list[TrialResult]:
    results: list[TrialResult] = []
    total = len(prompts) * trials
    n = 0
    with out.open("w") as f:
        for prompt in prompts:
            pid = prompt["id"]
            ptext = prompt["prompt"]
            for trial in range(1, trials + 1):
                n += 1
                client = McpClient(base, client_name=f"barrage-{pid}-t{trial}")
                t0 = time.monotonic()
                try:
                    await client.initialize()
                    rpc = await client.call_portfolio_ask(ptext)
                    struct, narr, is_err = parse_response(rpc)
                    r = score_trial(struct, narr, is_err)
                    r.error_message = None
                except Exception as e:
                    r = TrialResult(
                        prompt_id="", prompt_text="", trial=-1, exit_code=None,
                        duration_ms=None, wallclock_ms=0, has_ic_result=False,
                        has_hmac=False, narrative_chars=0, is_error=True,
                        error_message=f"{type(e).__name__}: {str(e)[:200]}",
                    )
                finally:
                    await client.aclose()
                r.prompt_id = pid
                r.prompt_text = ptext
                r.trial = trial
                r.wallclock_ms = int((time.monotonic() - t0) * 1000)
                results.append(r)
                f.write(json.dumps(asdict(r)) + "\n")
                f.flush()
                pass_marker = "✓" if (r.has_ic_result and not r.is_error and r.exit_code == 0) else "✗"
                print(
                    f"[{n:3}/{total}] {pass_marker} {pid} t{trial} "
                    f"wall={r.wallclock_ms}ms engine={r.duration_ms}ms "
                    f"ic_result={r.has_ic_result} hmac={r.has_hmac} "
                    f"narr={r.narrative_chars}c "
                    f"{('err: ' + r.error_message) if r.error_message else ''}",
                    flush=True,
                )
    return results


# ── parallel multi-stream ───────────────────────────────────────────


async def one_stream(
    stream_id: int,
    base: str,
    prompt: dict[str, Any],
    out: Path,
) -> TrialResult:
    pid = prompt["id"]
    ptext = prompt["prompt"]
    client = McpClient(base, client_name=f"parallel-s{stream_id}")
    t0 = time.monotonic()
    try:
        await client.initialize()
        rpc = await client.call_portfolio_ask(ptext)
        struct, narr, is_err = parse_response(rpc)
        r = score_trial(struct, narr, is_err)
        r.error_message = None
    except Exception as e:
        r = TrialResult(
            prompt_id="", prompt_text="", trial=-1, exit_code=None,
            duration_ms=None, wallclock_ms=0, has_ic_result=False,
            has_hmac=False, narrative_chars=0, is_error=True,
            error_message=f"{type(e).__name__}: {str(e)[:200]}",
        )
    finally:
        await client.aclose()
    r.prompt_id = pid
    r.prompt_text = ptext
    r.trial = stream_id
    r.wallclock_ms = int((time.monotonic() - t0) * 1000)
    with out.open("a") as f:
        f.write(json.dumps(asdict(r)) + "\n")
    return r


async def run_parallel(
    base: str,
    prompt_ids: list[str],
    prompts_by_id: dict[str, dict[str, Any]],
    out: Path,
) -> list[TrialResult]:
    out.write_text("")  # truncate
    selected = [prompts_by_id[pid] for pid in prompt_ids if pid in prompts_by_id]
    print(f"spawning {len(selected)} concurrent streams against same engine...", flush=True)
    t0 = time.monotonic()
    results = await asyncio.gather(
        *[one_stream(i + 1, base, p, out) for i, p in enumerate(selected)],
        return_exceptions=False,
    )
    wall_total = int((time.monotonic() - t0) * 1000)
    print(f"all {len(selected)} streams returned in {wall_total}ms wallclock", flush=True)
    for r in results:
        marker = "✓" if (r.has_ic_result and not r.is_error and r.exit_code == 0) else "✗"
        print(
            f"  {marker} stream{r.trial} {r.prompt_id} "
            f"wall={r.wallclock_ms}ms engine={r.duration_ms}ms "
            f"ic_result={r.has_ic_result} {('err: ' + r.error_message) if r.error_message else ''}",
            flush=True,
        )
    return list(results)


# ── summary ─────────────────────────────────────────────────────────


def write_summary(
    seq: list[TrialResult],
    par: list[TrialResult],
    out: Path,
    base: str,
    prompts_count: int,
    trials: int,
) -> None:
    pass_seq = sum(1 for r in seq if r.has_ic_result and not r.is_error and r.exit_code == 0)
    pass_par = sum(1 for r in par if r.has_ic_result and not r.is_error and r.exit_code == 0)
    fail_seq = [r for r in seq if not (r.has_ic_result and not r.is_error and r.exit_code == 0)]
    durs = [r.wallclock_ms for r in seq if r.has_ic_result and not r.is_error]
    avg_wall = int(sum(durs) / len(durs)) if durs else 0
    p50 = sorted(durs)[len(durs) // 2] if durs else 0
    p95 = sorted(durs)[int(len(durs) * 0.95)] if durs else 0

    lines = []
    lines.append(f"# v4.0 cobol barrage — {datetime.datetime.now().isoformat()}")
    lines.append(f"\nEndpoint: `{base}`")
    lines.append(f"Image: `mnemos-os/ic-engine:4.1.22-cpu-cpu` (1.11 GB)")
    lines.append(f"\n## Sequential — {prompts_count} prompts × N={trials}\n")
    lines.append(f"- **Pass:** {pass_seq}/{len(seq)} ({100*pass_seq/max(1,len(seq)):.1f}%)")
    lines.append(f"- **Fail:** {len(fail_seq)}")
    lines.append(f"- avg wallclock per trial: {avg_wall} ms")
    lines.append(f"- p50: {p50} ms  p95: {p95} ms")
    if fail_seq:
        lines.append("\n### Failures")
        for r in fail_seq[:30]:
            lines.append(
                f"- `{r.prompt_id}` t{r.trial}: "
                f"{r.error_message or 'no ic_result'} "
                f"(wall={r.wallclock_ms}ms, exit={r.exit_code})"
            )
    lines.append(f"\n## Parallel multi-stream — {len(par)} concurrent\n")
    lines.append(f"- **Pass:** {pass_par}/{len(par)}")
    for r in par:
        lines.append(
            f"- stream{r.trial} `{r.prompt_id}`: "
            f"{'✓' if (r.has_ic_result and not r.is_error and r.exit_code == 0) else '✗'} "
            f"wall={r.wallclock_ms}ms engine={r.duration_ms}ms"
        )
    lines.append("\n## Verdict\n")
    if pass_seq == len(seq) and pass_par == len(par):
        lines.append("✅ All prompts produced ic_result envelopes; multi-stream survived.")
    else:
        lines.append(
            f"⚠️ {len(seq) - pass_seq} sequential failures, "
            f"{len(par) - pass_par} parallel failures. See lists above."
        )
    out.write_text("\n".join(lines) + "\n")


# ── main ────────────────────────────────────────────────────────────


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--prompts", default=DEFAULT_PROMPTS)
    ap.add_argument("--trials", type=int, default=DEFAULT_TRIALS)
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--skip-sequential", action="store_true")
    ap.add_argument("--skip-parallel", action="store_true")
    args = ap.parse_args()

    prompts_data = json.loads(Path(args.prompts).read_text())
    prompts = prompts_data if isinstance(prompts_data, list) else prompts_data.get("prompts", [])
    prompts_by_id = {p["id"]: p for p in prompts}

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = Path(args.out_dir) if args.out_dir else Path(f"/tmp/v4-barrage-{ts}")
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"output: {out_dir}", flush=True)

    seq_results: list[TrialResult] = []
    par_results: list[TrialResult] = []

    if not args.skip_sequential:
        print(f"\n=== Sequential: {len(prompts)} prompts × N={args.trials} ===", flush=True)
        seq_results = await run_sequential(
            args.base, prompts, args.trials, out_dir / "sequential.jsonl"
        )

    if not args.skip_parallel:
        print(f"\n=== Parallel multi-stream: {len(PARALLEL_PROMPTS)} concurrent ===", flush=True)
        par_results = await run_parallel(
            args.base, PARALLEL_PROMPTS, prompts_by_id, out_dir / "parallel.jsonl"
        )

    write_summary(
        seq_results, par_results, out_dir / "summary.md",
        args.base, len(prompts), args.trials,
    )
    print(f"\n=== Done. Summary: {out_dir / 'summary.md'} ===", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
