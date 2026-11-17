# jscpd portability: node CLI vs Rust-port `cpd`, and the min-tokens "0 files" trap

The anti-erosion gate leans on jscpd. But "jscpd" is TWO different binaries in the wild, and
the quality-scan commands in `writing-code.md` were written for the node one. If your machine
has the Rust port, the commands change AND a silent trap appears. Verify which you have FIRST:

```bash
jscpd --version          # node CLI prints e.g. "jscpd 3.x/4.x"
                         # Rust port prints "cpd 5.0.12"  ← different tool
npx jscpd --version      # may resolve to the same Rust binary on Windows
```

## Flag differences (Rust port `cpd 5.x`)

| Concept | node jscpd (long) | Rust port `cpd 5.x` |
|---|---|---|
| threshold | `--threshold 10` | `-t 10` / `--threshold 10` |
| min lines | `--min-lines 3` | `-l 3` / `--min-lines 3` |
| min tokens | `--min-tokens 50` | `-k 50` / `--min-tokens 50` |
| formats | `--formats python` | `-f python` / `--format python` (NOTE: `--formats` errors) |
| full report | `--reporters console-full` | `-r console-full` |
| list formats | (n/a) | `--list` (shows `python`, etc.) |
| debug merged config | (n/a) | `--debug` (prints JSON config, exits) |

The long forms `--threshold/--min-lines/--min-tokens` are accepted by BOTH, so prefer them in
skill text. But `--formats` (plural) is node-only — the Rust port wants `--format` and errors
on `--formats` with `unexpected argument '--formats'`. When a command mysteriously fails on
flags, run `jscpd --help` and check which binary you're on.

## The silent "Files analyzed: 0" trap (min-tokens > file size)

**Symptom:** jscpd exits 0, "No duplicates found", table shows `Files analyzed: 0`,
`Total lines: 0` — even though the directory obviously has duplicated files. Easy to
misread as "no duplication / gate green". It is NOT green; it scanned NOTHING.

**Cause:** `--min-tokens N` is a per-BLOCK floor. If every file has fewer than N tokens,
no block qualifies and jscpd loads zero files. A 6-line Python handler is ~43 tokens; with
`--min-tokens 50` it is invisible. Drop to `-k 20` and the same 12 files suddenly report
76% dup / 11 clones. Same files, same duplication — the floor was just above the file size.

**Diagnosis one-liner:** rerun with `-r console-full` and read the `Files analyzed` cell.
`0` = your min-tokens (or a format/gitignore issue) is filtering everything out, not that the
code is clean. Confirm files are seen before trusting a "clean" result.

**Other zero-file causes to rule out:** (1) `.gitignore` is respected by default
(`no_gitignore: false` in `--debug`) — a broad ignore hides your files; pass `--no-gitignore`
to test. (2) extension not mapped — check `jscpd --list` for your language. (3) relative glob
under `handlers/` under-resolving on MSYS — run from inside the dir or use an absolute path.

## Consequence for building duplication test-fixtures

To make a copy-paste fixture that a specific jscpd command actually FLAGS, the duplicated
block must exceed `--min-tokens`. For `--min-tokens 50`, a trivial 5-line read loop is too
small (silently 0% / 0 files). Enlarge the shared body (more statements, same logic, behavior
preserved) until each block ≥ the token floor, then confirm the seed scan reports the expected
high dup% and `exit 1` BEFORE running any A/B. A fixture that reports 0% under the exact
command you'll grade with does not discriminate.

## Behavior-preservation note (Windows print)

Handlers that `print(line.rstrip())` will still show `\r` (`^M` under `cat -A`) because
Windows Python translates `\n`→`\r\n` on stdout. That is normal output translation, not a
bug — the 5 printed lines are still correct. Don't chase it as a behavior regression.
