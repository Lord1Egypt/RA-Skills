# mmx_recipe Pattern Reference

The `mmx_recipe` pattern is a thin, **typed** Python wrapper around the
[`mmx`](https://github.com/MiniMaxAI/cli) CLI that returns a structured
receipt for every invocation, optionally short-circuits to a dry run, and
attaches quota information to the call so the operator can audit cost
before the spend. The reference implementation lives at
[`~/youtube-studio/tools/mmx_recipe.py`](https://github.com/LuisCharro/youtube-studio)
(see `tools/mmx_recipe.py` in that repo).

This skill does **not** ship a parallel `mmx_recipe.py`. Its existing
[`scripts/generate_with_retry.py`](../scripts/generate_with_retry.py) is
the same pattern, specialised for `mmx music generate` and `mmx music
cover`. This document explains the pattern, points at the reference
implementation, and shows how to compose small operator scripts on top of
the existing skill surface.

> **Scope rule (Token Plan Plus, verified 2026-07-30).** The pattern
> documented here covers `mmx music` (generate + cover), `mmx speech`
> (synthesize + voices), and `mmx image` (generate). It does **not**
> cover `mmx video` — `mmx video generate` is exposed by the CLI but is
> **blocked on Plus** by a 3-hour rolling rate limit (Hailuo video is
> Max/Ultra only). See `references/minimax-generation-caveats.md` for
> the full Token Plan scope.

---

## What is `mmx_recipe`

A `mmx_recipe` is a Python module that:

1. Builds a typed `MMXReceipt` for every CLI call (argv, output path,
   stdout, stderr, return code, elapsed time, optional quota snapshot).
2. Exposes `dry=True` so the wrapper can build the argv and return a
   receipt **without** invoking `subprocess`. Useful for `--dry-run`
   preflights and CI.
3. Exposes `check_quota=True` so the wrapper attaches the live
   `mmx quota show --output json` snapshot to the receipt **before** the
   spend, so audit logs and dashboards show what was on hand when the
   call fired.
4. Raises a typed `MMXError(receipt)` so callers can inspect the
   receipt (stdout / stderr / rc / argv) instead of parsing a string
   exception.

The reference implementation supports `music`, `speech`, `image`,
`vision`, `video-sef` (subject-elevation-frame, the non-plus
alternative), and a `quota` subcommand.

---

## Why use it

The MiniMax CLI works fine when you only run a few commands, but it
falls short for the workflow this skill runs every day:

| Need | Raw `mmx` | With `mmx_recipe` pattern |
| --- | --- | --- |
| Verify quota before spending | Run `mmx quota show` separately, mentally join the two logs | `check_quota=True` attaches the snapshot to the receipt |
| Preview a command before spending | Print the command by hand; no audit trail | `dry=True` returns a receipt with `dry: True` and the argv |
| Recover after `SIGTERM`/`SIGKILL` post-save | Inspect stdout for `saved:` line, move the file by hand | Existing skill wrapper already does this (`generate_with_retry.py`) |
| Catch non-zero exit + missing output file | `subprocess.run` succeeds but the file is gone | `MMXError(receipt)` is raised with stdout/stderr attached |
| Retry transient failures only | No retry semantics in `mmx` | Existing wrapper retries on `code 5/6` / `timeout` / `network` markers |
| Audit one place per run | Spread across shell, Python, and the dashboard | One `MMXReceipt` per call is the audit trail |

The pattern is **complementary**, not a replacement, for the
`generate_with_retry.py` wrapper. The wrapper owns the mmx-music
operational contract (transient retry, `--timeout 600`, signal recovery,
file move). The `mmx_recipe` pattern owns the **shape of the return
value**, the **dry-run knob**, and the **quota snapshot attachment**.
`generate_with_retry.py` is the planned refactor target
([roadmap v1.1.5 item 17](../../music-craft-minimax_ROADMAP.md)) to expose
a `MMXReceipt`-style return and a `--dry` flag.

---

## The pattern structure

Every `mmx_recipe` module follows the same six-block shape:

```
┌──────────────────────────────────────────────────────────────┐
│ 1. ARGUMENT BUILDER                                           │
│    turn Python kwargs → argv list (flags + values)           │
├──────────────────────────────────────────────────────────────┤
│ 2. CORE SUBPROCESS RUNNER                                     │
│    resolve mmx on PATH; build full_argv; dry= or run         │
├──────────────────────────────────────────────────────────────┤
│ 3. QUOTA SNAPSHOT (optional, when check_quota=True)           │
│    mmx quota show --output json → dict attached to receipt    │
├──────────────────────────────────────────────────────────────┤
│ 4. RESULT WRAPPER                                             │
│    capture stdout/stderr/rc/elapsed → MMXReceipt              │
├──────────────────────────────────────────────────────────────┤
│ 5. FAILURE LIFT                                               │
│    rc != 0 OR expected output missing → raise MMXError(receipt)│
├──────────────────────────────────────────────────────────────┤
│ 6. PUBLIC WRAPPERS + CLI                                      │
│    one Python function per mmx subcommand; CLI maps them      │
└──────────────────────────────────────────────────────────────┘
```

The two invariants every wrapper preserves:

1. **`dry=True` never invokes `subprocess`.** The function returns a
   receipt with `dry=True` and the argv; nothing is downloaded, no
   quota is consumed, no file is written.
2. **`check_quota=True` snapshots quota before the spend.** The
   `mmx quota show --output json` call is synchronous (≤30 s) and
   captures the session state so the receipt shows what was available
   when the call ran.

---

## Reference implementation

The canonical reference is at `~/youtube-studio/tools/mmx_recipe.py`.
Three pieces define the contract:

### 1. The `MMXReceipt` dataclass

```python
@dataclass(frozen=True)
class MMXReceipt:
    command_run: list[str]
    output_path: Path | None
    stdout: str
    stderr: str
    returncode: int
    elapsed_seconds: float
    quota_cost: dict | None = None
    dry: bool = False
```

`frozen=True` so the receipt cannot be mutated after construction —
it is the audit trail and must be byte-stable. `quota_cost` is the
optional `mmx quota show --output json` payload captured before the
spend; `dry` distinguishes real runs from previews.

### 2. The `MMXError` exception

```python
class MMXError(RuntimeError):
    """Raised when mmx returns non-zero or the expected output file is missing."""
    def __init__(self, receipt: MMXReceipt) -> None:
        self.receipt = receipt
        detail = receipt.stderr.strip() or receipt.stdout.strip() or "unknown error"
        super().__init__(f"mmx failed (rc={receipt.returncode}): {detail}")
```

`self.receipt` lets callers inspect `stdout` / `stderr` / `command_run`
/ `elapsed_seconds` programmatically. No string-parsing of the
exception message.

### 3. The core `_run_mmx` runner

```python
def _run_mmx(
    argv: list[str],
    *,
    out_path: Path | None = None,
    dry: bool = False,
    check_quota: bool = False,
    timeout: int = 600,
) -> MMXReceipt:
    mmx_bin = shutil.which("mmx")
    if mmx_bin is None:
        raise MMXError(MMXReceipt(
            command_run=argv, output_path=out_path,
            stdout="", stderr="mmx binary not found on PATH",
            returncode=127, elapsed_seconds=0.0,
        ))
    full_argv: list[str] = [mmx_bin] + argv

    if dry:
        return MMXReceipt(
            command_run=full_argv, output_path=out_path,
            stdout="", stderr="", returncode=-1,
            elapsed_seconds=0.0, dry=True,
        )

    quota_cost: dict | None = None
    if check_quota:
        quota_cost = mmx_quota_show(dry=False)

    t0 = time.monotonic()
    result = subprocess.run(full_argv, capture_output=True, text=True, timeout=timeout)
    elapsed = time.monotonic() - t0

    receipt = MMXReceipt(
        command_run=full_argv, output_path=out_path,
        stdout=result.stdout, stderr=result.stderr,
        returncode=result.returncode, elapsed_seconds=elapsed,
        quota_cost=quota_cost,
    )

    if result.returncode != 0:
        raise MMXError(receipt)
    if out_path is not None and not Path(out_path).exists():
        raise MMXError(receipt)
    return receipt
```

Three behaviours that distinguish this from a plain `subprocess.run`:

- **`mmx` on `PATH` is resolved once.** Missing-binary is a typed error
  with rc=127, not a `FileNotFoundError` from the shell.
- **`check_quota` is a synchronous pre-call.** It cannot be backgrounded
  because the receipt must show the **pre-spend** state.
- **Missing output file is a typed error.** Even when `mmx` exits 0,
  if `out_path` does not exist, the receipt raises — this catches the
  real-world case where the CLI writes to `music_<timestamp>.mp3` in
  cwd regardless of `--out`.

### 4. The public wrappers

Each `mmx` subcommand has a small builder that converts Python kwargs
into argv and then delegates to `_run_mmx`. The `mmx music generate`
wrapper is the closest analog to what this skill needs:

```python
def mmx_music_generate(
    prompt: str,
    out_path: Path,
    *,
    instrumental: bool = True,
    model: str = "music-2.6",
    bpm: int = 60,
    key: str = "D minor",
    genre: str | None = None,
    mood: str | None = None,
    avoid: str | None = None,
    dry: bool = False,
    check_quota: bool = False,
    timeout: int = 900,
) -> MMXReceipt:
    argv = ["music", "generate", "--prompt", prompt, "--model", model,
            "--bpm", str(bpm), "--key", key]
    if instrumental:
        argv.append("--instrumental")
    if genre:
        argv.extend(["--genre", genre])
    if mood:
        argv.extend(["--mood", mood])
    if avoid:
        argv.extend(["--avoid", avoid])
    argv.extend(["--out", str(out_path)])
    return _run_mmx(argv, out_path=out_path, dry=dry,
                     check_quota=check_quota, timeout=timeout)
```

Keyword-only arguments after `*` mean the call sites stay readable,
and `dry` / `check_quota` / `timeout` are the three knobs the operator
is most likely to flip. The `mmx_quota_show` helper is its own small
function so wrappers can call it without depending on the rest of the
file:

```python
def mmx_quota_show(*, dry: bool = False) -> dict:
    mmx_bin = shutil.which("mmx")
    if mmx_bin is None:
        return {"error": "mmx binary not found on PATH"}
    if dry:
        return {"dry": True}
    result = subprocess.run(
        [mmx_bin, "quota", "show", "--output", "json"],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode == 0:
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {"raw": result.stdout.strip()}
    return {"error": result.stderr.strip(), "returncode": result.returncode}
```

Note the **graceful degradation**: if the CLI is missing or fails, the
helper returns a dict with `error` instead of raising. Callers that
attach `quota_cost` to a receipt must accept `{"error": ...}` as a
valid value.

---

## Adaptation for music-craft-minimax

This skill's `generate_with_retry.py` already covers the mmx-music
operational contract (transient retry on `code 5/6` and timeout /
network markers, `--timeout 600` default, signal recovery for
SIGTERM/SIGKILL after save, `--output-path` for the final file move).
The roadmap plans to fold the `MMXReceipt`-shaped return and the
`--dry` flag into the same wrapper
([v1.1.5 item 17](../../music-craft-minimax_ROADMAP.md)). Until that
lands, you can get the same ergonomics today by composing the existing
wrapper with a thin script that mirrors the `mmx_recipe` shape.

### Composition recipe

```python
# scripts/_mmx_recipe_compose.py (operator-side helper, NOT a new skill entry point)
"""Compose generate_with_retry.py with the mmx_recipe pattern.

This module is an example. It is not shipped with the skill — copy and
adapt for operator-side batch tooling that wants typed receipts and
dry-run preflights.
"""
from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

RETRY = Path(__file__).parent / "generate_with_retry.py"


@dataclass(frozen=True)
class MusicReceipt:
    command_run: list[str]
    output_path: Path
    stdout: str
    stderr: str
    returncode: int
    elapsed_seconds: float
    quota_cost: dict | None = None
    dry: bool = False
    expected_duration_seconds: int | None = None
    overwrite: bool = False


def mmx_quota_snapshot() -> dict | None:
    """Best-effort quota snapshot. Returns None if mmx is unavailable."""
    try:
        result = subprocess.run(
            ["mmx", "quota", "show", "--output", "json"],
            capture_output=True, text=True, timeout=30,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return {"error": result.stderr.strip(), "returncode": result.returncode}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"raw": result.stdout.strip()}


def run_music(
    mmx_args: list[str],
    output_path: Path,
    *,
    expected_duration_seconds: int | None = None,
    overwrite: bool = False,
    attempts: int = 3,
    dry: bool = False,
    check_quota: bool = False,
) -> MusicReceipt:
    """Run an mmx music command via generate_with_retry.py with typed return."""
    if not output_path:
        raise ValueError("output_path is required for music commands")

    argv = [sys.executable, str(RETRY), "--output-path", str(output_path)]
    if expected_duration_seconds is not None:
        argv.extend(["--expected-duration-seconds", str(expected_duration_seconds)])
    if overwrite:
        argv.append("--overwrite")
    argv.append("--")
    argv.extend(mmx_args)
    # Always keep --out on the mmx side; --output-path is the preservation target.
    if "--out" not in mmx_args:
        argv.extend(["--out", str(output_path)])

    quota_cost = mmx_quota_snapshot() if check_quota else None

    if dry:
        return MusicReceipt(
            command_run=argv, output_path=output_path,
            stdout="", stderr="", returncode=-1,
            elapsed_seconds=0.0, quota_cost=quota_cost, dry=True,
            expected_duration_seconds=expected_duration_seconds,
            overwrite=overwrite,
        )

    import time
    t0 = time.monotonic()
    proc = subprocess.run(argv, capture_output=True, text=True)
    elapsed = time.monotonic() - t0

    return MusicReceipt(
        command_run=argv, output_path=output_path,
        stdout=proc.stdout, stderr=proc.stderr,
        returncode=proc.returncode, elapsed_seconds=elapsed,
        quota_cost=quota_cost,
        expected_duration_seconds=expected_duration_seconds,
        overwrite=overwrite,
    )
```

The key design choice is that `dry=True` and `check_quota=True` work
the same way the reference implementation does: dry never invokes
`subprocess`, quota is captured before the spend. The wrapper still
delegates to `generate_with_retry.py` for the actual mmx invocation so
the skill's operational guarantees (transient retry, signal recovery,
file move) are preserved.

---

## Example scripts

These are **reference snippets**, not new files in the skill bundle.
Copy and adapt them for operator-side tooling that wants the
`mmx_recipe` ergonomics without waiting for the planned refactor
([v1.1.5 item 17](../../music-craft-minimax_ROADMAP.md)). Each one wraps
the existing `generate_with_retry.py` and follows the
`mmx_music_generate` shape from the reference implementation.

### 1. `generate-music.py` — basic generation

```python
#!/usr/bin/env python3
"""Generate one MiniMax music track with a typed receipt."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _mmx_recipe_compose import run_music, MusicReceipt


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Generate a MiniMax music track")
    p.add_argument("--prompt", required=True)
    p.add_argument("--lyrics")
    p.add_argument("--lyrics-file")
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--model", default="music-2.6")
    p.add_argument("--bpm", type=int)
    p.add_argument("--key")
    p.add_argument("--genre")
    p.add_argument("--mood")
    p.add_argument("--instrumental", action="store_true")
    p.add_argument("--avoid")
    p.add_argument("--expected-duration-seconds", type=int)
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--dry", action="store_true")
    p.add_argument("--check-quota", action="store_true")
    args = p.parse_args(argv)

    mmx_args = ["music", "generate",
                "--prompt", args.prompt, "--model", args.model, "--out", str(args.out)]
    if args.instrumental:
        mmx_args.append("--instrumental")
    else:
        if args.lyrics:
            mmx_args.extend(["--lyrics", args.lyrics])
        if args.lyrics_file:
            mmx_args.extend(["--lyrics-file", str(args.lyrics_file)])
    for flag, val in [("--bpm", args.bpm), ("--key", args.key),
                       ("--genre", args.genre), ("--mood", args.mood),
                       ("--avoid", args.avoid)]:
        if val is not None:
            mmx_args.extend([flag, str(val)])

    receipt: MusicReceipt = run_music(
        mmx_args, args.out,
        expected_duration_seconds=args.expected_duration_seconds,
        overwrite=args.overwrite,
        dry=args.dry, check_quota=args.check_quota,
    )

    if receipt.dry:
        print(f"DRY: {' '.join(receipt.command_run)}")
        return 0
    if receipt.returncode != 0:
        print(f"FAIL rc={receipt.returncode}", file=sys.stderr)
        if receipt.stderr.strip():
            print(receipt.stderr.strip(), file=sys.stderr)
        return receipt.returncode
    print(f"OK  rc={receipt.returncode}  {receipt.elapsed_seconds:.1f}s  out={receipt.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### 2. `cover-style.py` — cover / style transfer (upload-then-generate)

```python
#!/usr/bin/env python3
"""MiniMax cover / style transfer with a typed receipt.

Two paths:
- One-step: `mmx music cover --audio-file SRC --prompt STYLE --out OUT`
- Two-step: preprocess to get cover_feature_id, then generate with
  modified lyrics. (Not shown here — call the API directly per
  references/cover-workflow.md § Two-Step.)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _mmx_recipe_compose import run_music


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="MiniMax cover / style transfer")
    p.add_argument("--audio-file", required=True, type=Path,
                   help="Local source audio (MiniMax does not accept URLs)")
    p.add_argument("--prompt", required=True)
    p.add_argument("--lyrics")
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--instrumental", action="store_true")
    p.add_argument("--bpm", type=int)
    p.add_argument("--key")
    p.add_argument("--expected-duration-seconds", type=int)
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--dry", action="store_true")
    p.add_argument("--check-quota", action="store_true")
    args = p.parse_args(argv)

    if not args.audio_file.exists():
        print(f"ERROR: source audio not found: {args.audio_file}", file=sys.stderr)
        return 2

    mmx_args = ["music", "cover",
                "--audio-file", str(args.audio_file),
                "--prompt", args.prompt,
                "--out", str(args.out)]
    if args.instrumental:
        mmx_args.append("--instrumental")
    elif args.lyrics:
        mmx_args.extend(["--lyrics", args.lyrics])
    for flag, val in [("--bpm", args.bpm), ("--key", args.key)]:
        if val is not None:
            mmx_args.extend([flag, str(val)])

    receipt = run_music(
        mmx_args, args.out,
        expected_duration_seconds=args.expected_duration_seconds,
        overwrite=args.overwrite,
        dry=args.dry, check_quota=args.check_quota,
    )

    if receipt.dry:
        print(f"DRY: {' '.join(receipt.command_run)}")
        return 0
    if receipt.returncode != 0 or not receipt.output_path.exists():
        print(f"FAIL rc={receipt.returncode}", file=sys.stderr)
        return receipt.returncode or 1
    print(f"OK  cover={receipt.output_path}  {receipt.elapsed_seconds:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### 3. `batch-generate.py` — quota-aware batch

```python
#!/usr/bin/env python3
"""Quota-aware sequential MiniMax batch.

Reads a JSON list of {name, prompt, lyrics?, out, expected_duration_seconds?}
and runs each one through generate_with_retry.py, stopping when the
quota snapshot indicates exhaustion. Always sequential — see
references/minimax-generation-caveats.md § Sequential runs only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _mmx_recipe_compose import run_music, mmx_quota_snapshot


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Quota-aware sequential MiniMax batch")
    p.add_argument("--batch", required=True, type=Path,
                   help="JSON list of {name, prompt, out, ...}")
    p.add_argument("--max-items", type=int,
                   help="Stop after this many items even if quota allows more")
    p.add_argument("--stop-on-quota", action="store_true",
                   help="Snapshot quota between items and stop on exhaustion signal")
    p.add_argument("--dry", action="store_true")
    p.add_argument("--check-quota", action="store_true")
    args = p.parse_args(argv)

    items = json.loads(args.batch.read_text(encoding="utf-8"))
    if not isinstance(items, list):
        print("ERROR: --batch must be a JSON list", file=sys.stderr)
        return 2

    if args.check_quota and not args.dry:
        snapshot = mmx_quota_snapshot()
        if snapshot is None:
            print("WARNING: mmx quota snapshot unavailable; continuing", file=sys.stderr)
        else:
            print(f"quota_before_batch: {json.dumps(snapshot)[:200]}")

    results: list[dict] = []
    for index, item in enumerate(items, start=1):
        if args.max_items and index > args.max_items:
            print(f"reached --max-items={args.max_items}; stopping")
            break
        out = Path(item["out"])
        mmx_args = ["music", "generate",
                    "--prompt", item["prompt"], "--out", str(out)]
        if item.get("lyrics"):
            mmx_args.extend(["--lyrics", item["lyrics"]])
        if item.get("bpm") is not None:
            mmx_args.extend(["--bpm", str(item["bpm"])])
        if item.get("instrumental"):
            mmx_args.append("--instrumental")

        receipt = run_music(
            mmx_args, out,
            expected_duration_seconds=item.get("expected_duration_seconds"),
            overwrite=bool(item.get("overwrite", False)),
            dry=args.dry, check_quota=args.check_quota,
        )
        results.append({
            "name": item.get("name", f"item_{index}"),
            "returncode": receipt.returncode,
            "elapsed_seconds": round(receipt.elapsed_seconds, 1),
            "output_path": str(receipt.output_path),
            "dry": receipt.dry,
        })
        if receipt.returncode != 0:
            print(f"FAIL on {item.get('name', index)}: rc={receipt.returncode}",
                  file=sys.stderr)
            break

        if args.stop_on_quota and not args.dry:
            snap = mmx_quota_snapshot()
            if snap and snap.get("remaining", 1) <= 0:
                print("quota exhausted; stopping batch", file=sys.stderr)
                break

    print(json.dumps({"results": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### 4. `quota-check.py` — standalone quota checker

```python
#!/usr/bin/env python3
"""Standalone MiniMax quota check. Mirrors mmx_recipe.mmx_quota_show."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="MiniMax quota snapshot")
    p.add_argument("--timeout", type=int, default=30)
    p.add_argument("--quiet", action="store_true",
                   help="Print one-line summary only")
    args = p.parse_args(argv)

    try:
        proc = subprocess.run(
            ["mmx", "quota", "show", "--output", "json"],
            capture_output=True, text=True, timeout=args.timeout,
        )
    except FileNotFoundError:
        print("ERROR: mmx binary not found on PATH", file=sys.stderr)
        return 2
    except subprocess.TimeoutExpired:
        print(f"ERROR: mmx quota show timed out after {args.timeout}s",
              file=sys.stderr)
        return 3

    if proc.returncode != 0:
        print(f"ERROR rc={proc.returncode}: {proc.stderr.strip()}",
              file=sys.stderr)
        return proc.returncode
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        print(f"raw: {proc.stdout.strip()}")
        return 0

    if args.quiet:
        # Best-effort one-line summary; field names vary by mmx version.
        used = data.get("used_percent") or data.get("session_used_percent")
        remain = data.get("remaining_minutes") or data.get("session_remaining_minutes")
        window = data.get("window") or "5h"
        print(f"session: {window}  used={used}  remaining_minutes={remain}")
    else:
        print(json.dumps(data, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

The roadmap also plans to surface this snapshot inside
[`scripts/check_environment.py`](../scripts/check_environment.py) so the
existing preflight already returns quota-aware diagnostics
([v1.1.5 item 18](../../music-craft-minimax_ROADMAP.md)).

---

## Integration

### From the skill workflow

The skill's standard generation workflow already routes through
`generate_with_retry.py`:

```bash
python3 scripts/generate_with_retry.py \
  --output-path "$target_dir/M1_song.mp3" \
  -- \
  music generate \
  --prompt "..." \
  --model music-2.6 \
  --out "$target_dir/M1_song.mp3"
```

The `mmx_recipe` pattern adds two non-disruptive hooks:

```bash
# Dry-run preview: build argv, print receipt, no subprocess, no spend.
python3 scripts/generate_with_retry.py --dry ...

# Quota-aware run: snapshot quota before the spend, attach to log.
python3 scripts/generate_with_retry.py --check-quota ...
```

Both flags are planned in [v1.1.5 item 17](../../music-craft-minimax_ROADMAP.md).
Until they land, the example scripts in this document are the
operator-side stopgap.

### From operator-side batch tooling

When building batch tooling outside the skill:

1. Read prompts from a JSON file (see `batch-generate.py` example).
2. Snapshot quota once per batch (`mmx_quota_show`) and again between
   items if you want hard stops.
3. Always pass `--output-path` to `generate_with_retry.py` **and**
   `--out` to `mmx`. The wrapper output path is the preservation /
   verification destination; it does not replace the CLI's `--out`
   argument.
4. Verify every output with `ffprobe` before considering the batch
   successful — see
   [`references/minimax-generation-caveats.md`](minimax-generation-caveats.md#output-file-handling).
5. Treat the `MMXReceipt.quota_cost` field as audit evidence: it proves
   what was available when the call ran, **not** what was consumed by
   that specific call.

### From CI / preflight

```bash
# Build argv without spending quota.
python3 _mmx_recipe_compose.py --dry

# Snapshot quota without running anything.
python3 quota-check.py --quiet
```

Both should exit 0 on success even when nothing is generated, so a CI
job can gate on `--dry` argv shape and quota headroom independently.

---

## Troubleshooting

### `mmx: command not found`

The wrapper cannot resolve the `mmx` binary on `PATH`.

- Install the MiniMax CLI per the MiniMax install guide, then restart
  the shell.
- On Windows PowerShell, run `Get-Command mmx` after install; PATH may
  not update until the terminal is reopened.
- The reference wrapper returns `rc=127` with `stderr="mmx binary not
  found on PATH"` so callers can detect this without catching
  `FileNotFoundError`.

### `mmx quota show` fails or returns non-JSON

The CLI may be missing, returning an error, or returning unstructured
output. The reference wrapper returns `{"error": ...,
"returncode": ...}` or `{"raw": "<stdout>"}` instead of raising, so
the receipt stays valid even when the quota subsystem is unavailable.
Operator code should treat `quota_cost=None` and `quota_cost={"error":
...}` identically (no quota evidence).

### `--output-path` set but `--out` missing

`generate_with_retry.py` exits 2 with the explicit message:

> ERROR: --output-path does not replace mmx --out. Pass the same final
> audio path to the mmx command with --out, and keep --output-path for
> post-run preservation/verification.

This is intentional. The CLI may ignore `--out` (observed in field
runs where mmx writes to `$PWD/music_<timestamp>.mp3` regardless), so
the wrapper moves the file after the fact. If `--out` is missing on
the mmx side, the wrapper has no destination and refuses to run.

### `SIGTERM` / `SIGKILL` after a successful save

The wrapper classifies return codes `-15`, `-9`, `137`, `143` as
recoverable when this run created output. It verifies the file with
`ffprobe` (or an MP3 header check when `ffprobe` is missing), then
moves the file to `--output-path` and exits 0. This is not a bug; it
is the documented behaviour from
[`references/minimax-generation-caveats.md`](minimax-generation-caveats.md#output-file-handling).

### Output exists but is materially shorter than expected

`generate_with_retry.py --expected-duration-seconds N` warns when
`ffprobe` reports a duration below `0.7 * N`. This is a *warning*, not
an error: MiniMax cloud generation routinely returns 120–150 s for
lyric-heavy prompts even when longer is requested. See the duration
table in
[`references/minimax-generation-caveats.md`](minimax-generation-caveats.md#duration-is-a-target-not-a-guarantee).

### `dry=True` still shows `elapsed_seconds > 0`

If your wrapper composes multiple subprocesses (e.g. quota snapshot +
mmx invocation), `dry=True` must short-circuit **before** any
`subprocess.run`. The reference implementation does this in `_run_mmx`
before the `check_quota` block. If your version snapshots quota inside
`dry`, the snapshot itself is a real subprocess and burns a small
amount of quota.

### `dry=True` did not print the quota snapshot

`check_quota=True` requires a real subprocess. When `dry=True`,
`mmx_quota_show(dry=True)` returns `{"dry": True}` with no data — this
is by design so dry runs are byte-stable. If you need quota evidence in
a dry run, capture it in a separate `mmx_quota_show(dry=False)` call
before flipping to `dry=True`.

### Prompt byte limit rejected at 2079 bytes

The MiniMax API rejects prompts above 2000 UTF-8 bytes (warn at 1800).
`scripts/lint_music_request.py` already enforces this; run it before
the wrapper. Do **not** raise the prompt limit to work around this — use
`scripts/short-prompt-recipes.md` for compact prompt patterns instead.

---

## Related references

- [`references/mmx-flags-reference.md`](mmx-flags-reference.md) — full
  `mmx music generate` / `mmx music cover` flag table
- [`references/minimax-generation-caveats.md`](minimax-generation-caveats.md)
  — duration variance, sequential runs, signal-after-save recovery
- [`references/error-handling.md`](error-handling.md) — MiniMax-specific
  failure modes and recovery
- [`references/cover-workflow.md`](cover-workflow.md) — one-step vs
  two-step cover paths and consent
- [`references/short-prompt-recipes.md`](short-prompt-recipes.md) —
  compact prompt patterns that stay well below the 2000-byte limit
- [`scripts/generate_with_retry.py`](../scripts/generate_with_retry.py)
  — the existing wrapper that owns the mmx-music operational contract
- [`scripts/batch_cover.py`](../scripts/batch_cover.py) — sequential
  cover batch using `generate_with_retry.py`
- [`scripts/check_environment.py`](../scripts/check_environment.py) —
  environment preflight; planned to expose quota snapshot
  ([v1.1.5 item 18](../../music-craft-minimax_ROADMAP.md))
- [`music-craft-minimax_ROADMAP.md`](../../music-craft-minimax_ROADMAP.md)
  v1.1.5 — `MMXReceipt`-shaped return and `--dry` flag refactor target
  (item 17)
- `~/youtube-studio/tools/mmx_recipe.py` — canonical reference
  implementation
