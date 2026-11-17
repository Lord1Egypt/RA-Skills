# 10khr Runner — Heuristic Check Reference

_Exact string checks used by `critique_10khr_runner.py`'s `score_skill()` function._
_When grinding a skill to 50/50, use this to verify the runner will recognize your fix._

## D1: Frontmatter

| Check | Condition | Penalty |
|-------|-----------|---------|
| YAML parse failure | `yaml.safe_load(parts[1])` fails | -3 |
| Missing `name:` | `not fm.get("name")` | -2 |
| Missing `description:` | `not fm.get("description")` | -2 |
| `license` not in first 500 chars | `"license" not in content[:500].lower()` | -1 |
| Has `references/` but no `includes:` | `has_refs and "includes" not in str(fm)` | -1 |

**Key gotcha:** The `content[:500]` check means long YAML block-scalar descriptions push `license:` past position 500. Always place `license:` immediately after `name:`.

**Fix:** `license: MIT` on line 2, before description.

## D2: Description Quality

| Check | Condition | Bonus |
|-------|-----------|-------|
| Description > 50 chars | `len(desc) > 50` | +1 |
| Has "not for" (case-insensitive) | `"not for" in desc.lower()` | +1 |
| Has `triggers:` in frontmatter | `fm.get("triggers")` | +1 (capped at 5) |

**Baseline: 3.** Need all three bonuses for 5/5.

## D3: Conciseness (Code Ratio)

| Check | Condition | Score |
|-------|-----------|-------|
| Code ratio < 15% | `code_lines / total_lines < 0.15` | 5 |
| Code ratio < 20% | | 4 |
| Code ratio < 30% | | 3 |
| Code ratio ≥ 30% | | 2 |
| Total lines > 450 | | -1 penalty |

**Code lines** = lines where `l.strip().startswith("```")` (counts fence markers, not content between them).

## D4: Structure

| Check | Condition | Bonus |
|-------|-----------|-------|
| Has `references/` directory | `os.path.isdir(ref_dir)` | +1 |
| "when to read" in content | `"when to read" in content.lower()` | +1 |
| Total lines < 400 | `total_lines < 400` | +1 (capped at 5) |

**Baseline: 3.** Need all three for 5/5.

## D5: Instruction Clarity

| Check | Condition | Bonus |
|-------|-----------|-------|
| Has `## pipeline` or `## workflow` heading | in `content.lower()` | +1 |
| Has `## when to use` heading | in `content.lower()` | +1 |
| Has "example" anywhere | in `content.lower()` | +1 (capped at 5) |

**Baseline: 3.** Need all three for 5/5.

**Key gotcha:** The heading check is literal — `## When to Use` lowercases to `## when to use`. The word "example" anywhere in content triggers the bonus (section heading `## Examples` counts).

## D6: Freedom Calibration

| Check | Condition | Bonus |
|-------|-----------|-------|
| Has "why" or "because" | in `content.lower()` | +1 |
| Has "default" or "override" | in `content.lower()` | `min(5, d6)` (no-op if already 5) |

**Baseline: 4.** Need "why"/"because" for 5/5. The "default"/"override" check is a no-op ceiling, not a bonus.

## D7: Error Handling

| Check | Condition | Bonus |
|-------|-----------|-------|
| Has "gotcha" or "pitfall" | in `content.lower()` | +1 |
| Has "error" AND "handling" | both in `content.lower()` | +1 |

**Baseline: 3.** Need both for 5/5.

**Key gotcha:** Both words must appear — "error handling" as a phrase satisfies both checks. The section header `## Error Handling` triggers both bonuses.

## D8: Progressive Disclosure

| Check | Condition | Bonus |
|-------|-----------|-------|
| Has ≥3 `.md` files in `references/` | `len(ref_files) >= 3` | +1 |
| "when to read" in content | in `content.lower()` | +1 |

**Baseline: 3.** Need both for 5/5.

**Key gotcha:** Minimum 3 reference files required for the bonus. Two well-organized refs aren't enough.

## D9: Scripts Quality

The runner scans **ALL** scripts (not just the first 3) for `--help`/`usage`/`argparse`. First 3 only were sampled before 2026-07-14 — that hid real gaps.

- No scripts directory → **5/5 (N/A)**
- Scripts dir present but empty → **4/5**
- Has scripts; `missing_help` ≥ half of all scripts → **3/5**
- Has scripts; `missing_help` < half → **4/5**
- Has scripts; every script has `--help`/`usage`/`argparse` → **5/5**

Note: the check is a literal match on the strings `--help`, `usage`, or `argparse` anywhere in the file. A hand-rolled usage block without those tokens will score as missing — confirm manually with `python3 <script> --help`.

**Two REAL D9 traps caught by the manual `--help` test (2026-07-18 grind):**
- **Bash `--help` branch that omits `exit 0` fails D9.** A `set -u` script whose `--help|-h)` case sets `TARGET="."` and `echo`s usage but does NOT `exit 0` continues PAST the `case` into the main body — e.g. `if [ ! -d "$TARGET/.git" ]; then echo "No .git..."; exit 2; fi` — so `bash script.sh --help </dev/null` prints usage AND exits 2, not 0. The runner's real D9 test (`bash script.sh --help </dev/null; echo $?`) then reports rc=2 and the heuristic scores D9 as failed even though usage printed. **The only valid bash `--help` branch ENDS with `exit 0` before any positional/main logic.** Found + fixed: `ocas-skilllab/scripts/secret-scan.sh` (branch set `TARGET` and echoed but lacked `exit 0` → rc=2; added `exit 0 ;;`).
- **Renaming `sys`→`_sys` for the Python guard leaves stale `sys.` references.** The skill's guard example uses `import sys as _sys`. If you apply it but `main()` (or any function) still calls `sys.argv`, Pyright/linters flag `sys is not defined` and the script breaks at load. Either (a) update EVERY `sys.` reference in the file to `_sys.`, or (b) simpler — keep `import sys` (no rename) and write the guard as `if set(sys.argv[1:]) & _HELP_ARGS: print(...); sys.exit(0)`. The rename buys nothing. Found + fixed: `ocas-custodian/scripts/verify_kanban_env.py` (renamed import, then had to fix `home = sys.argv[1]` → `_sys.argv[1]`).

## D10: Completeness

| Check | Condition | Bonus |
|-------|-----------|-------|
| Has "gotcha" or "pitfall" | in `content.lower()` | +1 |
| Has "when not to use" | in `content.lower()` | +1 |

**Baseline: 3.** Need both for 5/5.

**Key gotcha:** "when not to use" is the exact literal string. `## When NOT to Use` lowercases to `## when not to use` and triggers the bonus.

**Efficiency:** A single combined heading `## When to use / When NOT to use` satisfies BOTH D5's `## when to use` check AND D10's `when not to use` check at once (it contains `## when to use` as a substring and `when not to use` verbatim). Write one combined section instead of two separate ones — saves tokens and closes two dimensions simultaneously. Confirmed in the 2026-07-22 `util-apibuild` grind: one combined section moved D5 4→5 and D10 4→5 (and D1 5 came from moving `license:` to line 2).

---

## Scoring Summary Table

| Dim | Baseline | Need for 5/5 | Exact trigger |
|-----|----------|--------------|---------------|
| D1 | 5 | Fix deductions | `license` in first 500 chars, `includes:` if refs exist |
| D2 | 3 | All 3 bonuses | >50 chars, "not for", `triggers:` |
| D3 | 5 | Code ratio <15% | Under 20% is 4, under 30% is 3 |
| D4 | 3 | All 3 bonuses | Has refs, "when to read", <400 lines |
| D5 | 3 | All 3 bonuses | `## when to use` heading, "example" anywhere |
| D6 | 4 | +1 | "why" or "because" anywhere in content |
| D7 | 3 | Both bonuses | "pitfall"/"gotcha" + "error"+"handling" |
| D8 | 3 | Both bonuses | ≥3 ref files + "when to read" |
| D9 | 5 | N/A if no scripts | Else scan ALL scripts: 5/5 only if every script has `--help`/`usage`/`argparse`; <half missing → 4, ≥half missing → 3; empty dir → 4 |
| D10 | 3 | Both bonuses | "pitfall"/"gotcha" + "when not to use" |

## Common Failure Patterns

1. **D1 false deduction:** Long YAML description pushes `license:` past char 500 → place `license:` on line 2
2. **D5 stuck at 4:** Missing `## when to use` heading (having the content under another heading name doesn't count)
3. **D6 stuck at 4:** No "why"/"because" explanation for rigid rules
4. **D8 stuck at 4:** Only 2 reference files instead of 3
5. **D10 stuck at 4:** No "when not to use" literal phrase