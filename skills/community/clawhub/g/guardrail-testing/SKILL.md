---
name: guardrail-testing
description: Prove an agent guardrail refuses — fail-closed exit codes, hostile fixtures, mutation tests without stale-.pyc false greens. Use when adding a gate or filter. Runs your tests, writes temp files, mutates code only in a mktemp copy, never in place. Trigger on "test my guardrail", "does this gate fail closed", "mutation testing", "the test passes but the guard is broken".
metadata: {"clawdbot":{"emoji":"🧪","requires":{"bins":["python3","bash"]},"homepage":"https://openclaw.ai"}}
---

# Guardrail Testing

A guardrail you have never watched refuse is not a guardrail. Proof takes three facts: a hostile input is refused, the refusal disappears when the guard is deleted, and the deleted guard was really the code that ran.

## When to Use

| Trigger | Action |
|---|---|
| "I added a gate / filter / allowlist to the agent" | §1 contract, §2 one hostile fixture per branch, §3 mutate |
| "The tests pass, is the guard actually tested?" | §3 `mutate.py`: a survivor means no test needs that block |
| "Mutation run says 100 % killed" on Python | §4: rule out the stale `.pyc` first |
| "The filter never blocked anything in prod" | §2 + §7: feed it the forbidden input, accented and encoded |
| Bash guard returns 0 where it should stop | §5: the three shell traps |

## What This Skill Runs

| Piece | Touches |
|---|---|
| `scripts/mutate.py` (stdlib, Python 3.8+) | Copies your repo into a new `mktemp -d` per run, rewrites the guard file **in the copy only**, runs your test command there, deletes the copies, and exits 3 if the original file's SHA-256 changed. No network. Never writes inside your repo. |
| Snippets below | Run your tests and write fixtures under `mktemp -d`. Nothing modifies source in place. |

```bash
M="<this skill's directory>/scripts/mutate.py"
python3 "$M" --selftest
# Output: 13 checks, last line: SELFTEST: PASS   (exit 1 on any failure)
```

## 1. The Exit-Code Contract

| Code | Meaning | Caller does |
|---|---|---|
| 0 | Verified allowed | Proceed |
| 2 | Refused on purpose (policy said no) | Stop, log the reason |
| 3 | Indeterminate: state unreadable, input absent, zero files read | Stop. **Never** mapped to 0 |
| 1, 126, 127, 128+n | Crash, not found, signal (Python traceback = 1, argparse usage error = 2) | Stop: anything not 0 is a refusal |

```bash
bash ./gate.sh "$state"; rc=$?
if [ "$rc" -eq 0 ]; then do_the_thing; else echo "gate refused rc=$rc" >&2; exit "$rc"; fi
# NOT: [ "$rc" -ne 2 ] && do_the_thing   (a crash exits 1 and walks through)
```

A tool that also emits 2 for its own usage errors collides with "refused". `mutate.py` overrides `argparse.error` to exit 3, and wraps `main()` so a crash is 3, never a verdict.

## 2. Hostile Fixtures: One per Branch, Isolated

Each fixture must be refusable by **exactly one** check. If the fixture for check B is also refused by check A, deleting B changes nothing and B's mutant survives while B is fine; worse, a broken B looks proven.

| Input class | Fixture | Must return |
|---|---|---|
| Absent | argument/env/param not passed at all | 3 |
| Empty / whitespace | `""`, `" "`, empty file | 3 |
| Null / wrong type | `None`, `null`, list where string expected | 3 |
| Unreadable state | missing file, `chmod 000`, invalid JSON | 3 |
| Zero inputs read | glob matched nothing, loop never ran | 3 |
| Forbidden value | the thing the guard exists to stop | 2 |
| Duplicated parameter | `f=body&f=id` | 2 |
| Encoded name / value | `%24select=`, accented forbidden word | 2 |
| Allowed baseline | one input that must pass | 0 |

Fail-opens found only by executing, never by review:

| Trap | Why review misses it | Fixture that catches it |
|---|---|---|
| Query guard validates a field list only **if the param is present** | Absent param = server default = every field, body included | Request with no field-list param → refused |
| Duplicated param: guard reads the last value, the server may read the first or merge them | `dict(parse_qsl(q))` silently keeps the last one | `$select=body&$select=id` and `%24select=body&$select=id` → refused |
| Webhook verifier used as a boolean | svix `Webhook.verify` (1.96.1, run 2026-09-30) throws on a bad signature and **returns the parsed payload** (body `null` → `null`); a mocked verify returns `undefined` | Real library, forged signature → handler rejects; valid signature with body `null` → accepted |
| Mutant survives because the hostile fixture fails for another reason | The test still sees "refused", from the wrong guard | Fixture that passes every other check (§3 `--expect` for the reverse case) |

```python
from urllib.parse import parse_qs, parse_qsl
q = "%24select=body&$select=id"
print(parse_qs(q), dict(parse_qsl(q)))
# Output: {'$select': ['body', 'id']} {'$select': 'id'}
# Rule: any name seen twice, or not in the allowlist after decoding → refuse.
```

## 3. Mutation by `FAIL-CLOSED` Block

Wrap each refusal in markers. `mutate.py` replaces one block at a time with a no-op (`pass`, `:`, `;`) and expects the tests to fail. A block must be a whole statement: a `case` arm or half an `if` gives an `INVALID` mutant (exit 3).

```bash
#!/usr/bin/env bash
# gate.sh <state-file> : 0 proceed, 2 refuse, 3 indeterminate. Never 0 on doubt.
set -uo pipefail
state="${1-}"
# FAIL-CLOSED unreadable or empty state
[ -r "$state" ] && [ -s "$state" ] || { echo "REFUSE: unreadable" >&2; exit 3; }
# END-FAIL-CLOSED
[ "$(head -n1 "$state")" = "ok" ] && exit 0
# FAIL-CLOSED anything but "ok" refuses
echo "REFUSE: not ok" >&2; exit 2
# END-FAIL-CLOSED
exit 0
```

Test fixtures, one per block: `ok` → 0, empty file → 3, missing file → 3, `maybe` → 2 (readable, so only block 2 can refuse it).

```bash
python3 "$M" --repo . --file gate.sh --test "bash tests/test-gate.sh" --expect 'KO want='
# Output:
# mutate: baseline PASS
# mutate: canary KILLED (tests load the copied file)
# mutant 1  KILLED    rc=1  block L5 # FAIL-CLOSED unreadable or empty state (replay: KILLED)
# mutant 2  KILLED    rc=1  block L9 # FAIL-CLOSED anything but "ok" refuses (replay: KILLED)
# RESULT: 2/2 killed, each replayed on a fresh copy -> exit 0
```

Same run after deleting the `maybe` fixture: `mutant 2  SURVIVED  rc=0` → `exit 2`.

| Check inside `mutate.py` | Why | On failure |
|---|---|---|
| Baseline green on an unmutated copy | A kill on red tests proves nothing | 3 |
| Canary (`raise SystemExit` / `exit 97` / `throw` at top) must break the tests | Proves the tests load the **copied** file, not an installed or absolute-path one | 3 |
| New copy + empty `PYTHONPYCACHEPREFIX` per run | §4 | — |
| Every kill replayed on a second fresh copy | A green is only trusted twice | `FLAKY` → 3 |
| `--expect REGEX` must match the failing output | Kill must come from the named assertion, not an import error | `KILLED-ELSEWHERE` → 3 |
| Syntax check of the mutant (`compile`, `bash -n`, `node --check`) | A mutant that does not parse is killed for the wrong reason | `INVALID` → 3 |
| `--sub OLD NEW` must match exactly once | Ambiguous mutation | 3 |

## 4. The Stale `.pyc` False Green

CPython revalidates a timestamp `.pyc` on **source mtime in whole seconds + source size**. Two same-size versions of a file written in the same second: the second run executes the first one's bytecode. Verified 2026-09-30, macOS 26.6, Apple `/usr/bin/python3` 3.9.6 and Homebrew 3.14.7:

| Condition, source rewritten same size + same second | Code executed |
|---|---|
| Nothing done | **old** (5/5 natural back-to-back writes, both interpreters) |
| `PYTHONDONTWRITEBYTECODE=1` alone | **old**: it stops writing, still reads the stale file |
| `rm -rf __pycache__` on Homebrew Python | new |
| `rm -rf __pycache__` on Apple `/usr/bin/python3` | **old**: its `sys.pycache_prefix` is `~/Library/Caches/com.apple.python`, not `__pycache__` |
| Fresh empty `PYTHONPYCACHEPREFIX` | new, both interpreters |
| pytest 9.1.1 test file mutated, `-p no:cacheprovider` | **old**: a failing test reports PASS. The flag only disables `.pytest_cache`; the assertion-rewrite `.pyc` is still stale |

```bash
python3 -c 'import sys; print(sys.pycache_prefix)'   # know where your cache lives first
# Output (Apple python3): /Users/<you>/Library/Caches/com.apple.python
```

Rules: new copy or empty `PYTHONPYCACHEPREFIX` per run, plus `PYTHONDONTWRITEBYTECODE=1`, plus `__pycache__` purged, 1 s between writes (`--gap`, default 1.0), and every green replayed in isolation. The selftest reproduces the naive loop reporting 2/2 killed while one mutant survives, then shows `mutate.py` reporting the survivor with `--gap 0`.

## 5. Three Bash Traps (verified 2026-09-30, bash 3.2.57)

| Trap | Effect |
|---|---|
| Function redefined **after** the script's call site (stub or mutant appended at the end) | The original already ran: the stub never applies, the mutant is a no-op |
| `local x="$(f)"` | `$?` is the status of `local` (0), not of `f` |
| `die` / `exit` inside `$(…)` | Kills the subshell only; the caller continues with an empty value, even under `set -e` when combined with `local` |

```bash
f(){ echo partial; return 3; }
a(){ local x="$(f)"; echo "rc=$?"; };  b(){ local x; x="$(f)"; echo "rc=$?"; };  a; b
# Output: rc=0 / rc=3
die(){ echo "FATAL: $*" >&2; exit 2; }
token(){ [ -r /nonexistent/token ] || die "no token"; }
t="$(token)"; echo "still running, token='$t'"
# Output: FATAL: no token / still running, token=''   (script exit 0)
```

Fix: declare then assign (`local x; x="$(f)" || exit 3`), guard every `$(…)` that can die, stub functions **before** sourcing, and only call `main` when executed: `[ "${BASH_SOURCE[0]}" = "$0" ] && main "$@"`.

## 6. Test Preamble: Sandbox or Stop

Every test sources this before its first assertion. A variable left unset silently falls back to the production default.

```bash
PROD_STATE="$HOME/.myagent/state"                  # captured once; tests may rewrite $HOME later
SANDBOX="$(mktemp -d)" || exit 1; chmod 700 "$SANDBOX"; trap 'rm -rf "$SANDBOX"' EXIT
export STATE_DIR="$SANDBOX/state" ALLOWLIST="$SANDBOX/allowlist.test"
for v in STATE_DIR ALLOWLIST; do                   # check BEFORE the first mkdir or write
  case "${!v}" in "$PROD_STATE"*) echo "STOP: $v points at production" >&2; exit 1 ;; esac
  case "${!v}" in /tmp/*|/private/tmp/*|/var/folders/*|/private/var/folders/*) ;;
    *) echo "STOP: $v escapes the sandbox: ${!v}" >&2; exit 1 ;; esac
done
mkdir -p "$STATE_DIR"; printf 'box-a@example.test\n' > "$ALLOWLIST"   # RFC 2606 domain, never real
# Output with STATE_DIR forced to $HOME/.myagent/state/mail: STOP: STATE_DIR points at production (exit 1, nothing created)
```

Resolve the path the code will actually compute (`${STATE_DIR:-${ALT:-$HOME/...}}`), not only the variable you set: one module that reads a variable you did not export writes to production. Before this, a test depending on the real allowlist file went red in 36 places after an unrelated change, and a mutation test stopped proving anything because the refusal came from the missing file, not from the guard under test.

## 7. Two More Silent Fail-Opens

**`iconv //TRANSLIT` on macOS** (verified 2026-09-30, macOS 26.6, `/usr/bin/iconv`): it prefixes the accent instead of removing it, prints a warning, exits 1, and still outputs text, so a `[ -n "$out" ]` fallback never fires.

```bash
printf 'spécialiste' | iconv -f UTF-8 -t ASCII//TRANSLIT 2>/dev/null | grep -qi specialist && echo MATCH || echo "NO MATCH"
# Output: NO MATCH   (arrêt → arr^et, n°1 → n^01)
```

Replace with an explicit table, and keep a regression fixture that feeds the accented forbidden word:

```bash
deaccent(){ LC_ALL=C.UTF-8 sed 'y/àâäéèêëîïôöùûüçÀÂÉÈÊËÎÏÔÙÛÜÇ/aaaeeeeiioouuucAAEEEEIIOUUUC/; s/œ/oe/g; s/°/o/g'; }
printf 'spécialiste n°1 Élève' | deaccent
# Output: specialiste no1 Eleve
# Under LC_ALL=C, BSD sed rejects the table ("transform strings are not the same length"), exits 1 and prints nothing: check its status.
```

**Secrets in argv**: `-H "Authorization: …"`, `-u user:pass`, `-passin pass:…` are readable by any local user in `ps -ww -o args=`. Pass them on stdin (`curl -K -`, `-passin env:VAR`). Scanner, fail-closed on zero files; the `[A]` classes keep it from matching its own source:

```bash
root="${1:-.}"
[ -n "$(find "$root" -type f \( -name '*.sh' -o -name '*.py' -o -name '*.js' \) | head -1)" ] \
  || { echo "scanned 0 files" >&2; exit 3; }
grep -rnE --include='*.sh' --include='*.py' --include='*.js' \
  -e '(-H|--header)[[:space:]]+["'"'"']?[A]uthorization:' -e '-pass(in|out)[[:space:]]+[p]ass:' \
  -e 'curl[^|]*[[:space:]](-u|--user)[[:space:]]+[^[:space:]]+:[^[:space:]]' "$root"
case $? in 0) exit 2 ;; 1) exit 0 ;; *) exit 3 ;; esac   # grep 2 = read error: never "clean"
# Output: ./bin/bad.sh:1:curl -sS -H "Authorization: Bearer $TOKEN" ...  (exit 2); missing dir: scanned 0 files (exit 3)
```

Do not pipe `find | xargs grep`: `xargs` does not pass grep's status through (macOS: "no match" and "read error" both come back as 1; GNU: 123), so an unreadable file reads as clean.

## Output Format

```
GUARDRAIL PROOF — <guard file> — <date>
Contract: 0 proceed / 2 refuse / 3 indeterminate — caller proceeds on 0 only: <yes/no>
Fixtures: <n> hostile (one per branch, isolated), <n> allowed baseline
Mutation: <k>/<n> killed, replayed on fresh copies | canary killed | baseline green
Survivors: <block line + what no test requires>   (or: none)
Stale-bytecode defence: fresh copy + empty PYTHONPYCACHEPREFIX (python only)
VERDICT: PROVEN | NOT PROVEN (exit 2) | INDETERMINATE (exit 3)
```

```
GUARDRAIL PROOF — gate.sh — 2026-09-30
Contract: 0 proceed / 2 refuse / 3 indeterminate — caller proceeds on 0 only: yes
Fixtures: 3 hostile (one per branch, isolated), 1 allowed baseline
Mutation: 2/2 killed, replayed on fresh copies | canary killed | baseline green
Survivors: none
VERDICT: PROVEN
```

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| `canary SURVIVED` → exit 3 | Tests import an installed copy or an absolute path | Import relative to the repo root; use `{root}` in `--test` |
| `INVALID` mutant | Block covers half a statement (`case` arm, `elif`) | Move markers around a complete statement |
| `KILLED-ELSEWHERE` | Failure came from an import error or another assertion | Name assertions (`"REFUSE-BODY"`) and pass `--expect` |
| Mutant survives but the guard looks right | Hostile fixture refused by another check | Build a fixture that passes every other check |
| Green on Python after a same-size edit | Stale `.pyc` (§4) | Run through `mutate.py` or set an empty `PYTHONPYCACHEPREFIX` |
| `baseline is not green` | Tests already red, or depend on a file outside the repo | Fix first; §6 preamble |
| Slow run | One full copy per mutant | `--ignore node_modules --ignore .venv` if the tests do not need them |

## Scope

This skill ONLY:
- runs your test command against copies of your repo inside `mktemp -d`, and deletes them;
- mutates code in those copies, one block or one `--sub` at a time;
- reports survivors and exits 0 / 2 / 3.

This skill NEVER:
- edits, formats or restores a file in your working tree (it checks the original SHA-256 instead);
- treats a timeout, a crash, a red baseline or a surviving canary as a pass;
- sends anything over the network, or reads secrets.
