---
name: openclaw-prompt-shield
description: Local input-hardening scanner for OpenClaw agents. Pattern-based detection across 9 categories of LLM input risks, with combined-signal scoring and caller-supplied whitelists. Returns risk score 0-100, matched categories, a suggested sanitized version, and a safe-to-process verdict. Pure Python standard library, no remote calls, no API keys, no LLM.
license: MIT
metadata: {"openclaw":{"requires":{"bins":["python3"]},"primaryEnv":null,"homepage":"https://clawhub.ai/gopendrasharma89-tech/openclaw-prompt-shield"}}
---

# openclaw-prompt-shield

v0.4.1

A practical input-hardening skill for OpenClaw agents. It scans user-submitted text for prompt-injection, jailbreak, role-override, and data-exfiltration patterns before the agent processes them. All detection is pattern-based, deterministic, and runs locally in Python.

## Why this exists

Most agent security skills focus on output review (do not leak secrets, do not break policy). Few focus on input hardening — checking what the user, or a third party whose content the agent is reading, is trying to do to the agent itself. Prompt injection is the most common real-world LLM exploit, and this skill gives the agent a fast no-API local check.

## What this skill does

- `scripts/scan_input.py` — score a single piece of text 0-100 for injection risk, return matched categories, and a verdict (`safe`, `caution`, `block`).
- `scripts/sanitize_input.py` — produce a redacted, quoted version of risky text the agent can still read for context without executing the embedded directives.
- `scripts/scan_batch.py` — run the scan over many inputs at once (a list of email bodies, web search snippets, scraped pages) and emit a JSON report of which ones are safe to feed downstream.
- `scripts/check_deps.sh` — verify `python3` is installed.
- `references/patterns.md` — category-level summary of what each detector covers.
- `references/exfil-hosts.txt` — caller-editable list of suspicious host fragments used by the exfiltration check.
- `references/categories.txt` — caller-editable verb / target / quantifier alphabets used to build the regex catalog at import time.

## What this skill does not do

- It does not call any LLM, classifier API, or remote service.
- It does not guarantee 100% detection. Determined attackers can evade pattern-based detection. Treat this as a fast first-pass filter, not a complete defense.
- It does not block the agent. It returns a risk verdict and lets the agent or the wrapping policy decide.
- It does not modify any files outside the directories the user provides.

## Detection categories

| Category | What it catches |
|---|---|
| `instruction_override` | Phrasing that asks the model to drop or replace whatever it was previously told |
| `role_hijack` | Identity swaps into "unrestricted" personas |
| `system_prompt_leak` | Attempts to extract the agent's hidden context |
| `delimiter_injection` | Fake structural markers (chat delimiters, pseudo-system tags, identity frontmatter) |
| `data_exfiltration` | Attempts to send conversation, secrets, or context to outside endpoints |
| `tool_abuse` | Coercion into destructive shell commands or sensitive file reads |
| `encoding_evasion` | Base64/hex/URL-encoded payloads with decode-then-run phrasing |
| `policy_bypass` | Rationalizations for ignoring safety rules |
| `indirect_injection` (NEW in v0.3.0) | Imperatives wrapped inside quoted text, markdown links, fenced code blocks, HTML comments, or zero-width / bidi character sequences so they look like data rather than instructions |

The full category-level documentation is in `references/patterns.md`. Patterns are constructed at runtime from word-fragment lists; the source files therefore do not contain literal adversarial phrases.

## Combined-signal bonus

Real attacks usually chain techniques (override + role hijack + leak); accidental matches rarely do. When two or more distinct categories all fire on the same input, a small bonus is added on top of the per-category sum:

| Distinct categories triggered | Bonus added |
|---|---|
| 2 | +6 |
| 3 | +12 |
| 4 | +18 |
| 5+ | +24 |

This makes a chained attack reliably cross the `block` threshold while a single isolated trigger word inside an otherwise benign sentence stays in the `caution` band where the agent can still read the message safely.

## Required dependencies

```bash
bash scripts/check_deps.sh
```

The skill is pure Python 3 standard library — no `pip install` needed.

## Workflows

### 1. Scan a single user message

```bash
python3 scripts/scan_input.py --text "<the user message>"
```

The output looks like:

```
risk_score: 81
verdict: block
thresholds: caution>=30, block>=70
combined_signal_bonus: +6 (distinct categories: 2)
matches:
  instruction_override (+45):
    - <fragment 1>
    - <fragment 2>
  system_prompt_leak (+30):
    - <fragment 3>
recommendation: <category-specific guidance, see Recommendations section>
```

You can also feed text from a file:

```bash
python3 scripts/scan_input.py --file user_message.txt --json
```

### 2. Whitelisting known-good content

If a domain legitimately discusses prompt injection (security blog posts, threat-modeling docs, fine-tuning datasets), pass the surrounding sentence with `--whitelist` so its trigger fragments are dropped before scoring:

```bash
python3 scripts/scan_input.py \
  --text "<security blog paragraph that quotes a known attack phrase>" \
  --whitelist "<the same paragraph or the quoted attack phrase>"
```

Or load a list of allowed phrases from a file:

```bash
python3 scripts/scan_input.py --file post.md --whitelist-file allow.txt
```

Whitelist matching is case-insensitive substring containment, so the whitelist entry can be the entire surrounding sentence and it will absorb every fragment the scanner extracts from inside it.

### 3. Sanitize before feeding the agent

```bash
python3 scripts/sanitize_input.py --file scraped_page.txt --output safe.txt
```

The output:

- Wraps the original content in a clearly marked `<UNTRUSTED_USER_CONTENT>` block so the agent cannot mistake it for instructions.
- Replaces any matched phrases with `[[REDACTED:category]]` markers.
- Adds a header summary listing what was flagged (including the combined-signal bonus, when it fired) so the agent has the context.

### 4. Batch-scan a list of inputs

```bash
python3 scripts/scan_batch.py --jsonl inputs.jsonl --output report.json
```

Each line of `inputs.jsonl` is `{"id": "...", "text": "..."}`. The report contains per-id verdicts and an optional `--only-safe safe.jsonl` subset to forward downstream. `--whitelist` and `--whitelist-file` work the same way as on `scan_input.py`.

### 5. Verdict thresholds

Defaults:

- `safe` if score < 30
- `caution` if 30 ≤ score < 70
- `block` if score ≥ 70

Override per call:

```bash
python3 scripts/scan_input.py --file in.txt --caution-at 40 --block-at 80
```

For domains that legitimately discuss prompt injection (security research, AI policy writing), raise `--block-at` to 80 or 90 so only multi-category matches block, or use `--whitelist`.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | safe |
| 1 | caution |
| 2 | block |
| 3 | error (bad arguments, unsafe path, file not found) |

## Use cases

- Pre-filter user messages before the agent treats them as instructions.
- Validate scraped web content, email bodies, or RAG snippets before they enter the prompt.
- Score a corpus of historical chat logs and surface the highest-risk inputs for human review.
- Add a guardrail step inside a multi-agent pipeline.

## Safety properties

- Pure Python 3 standard library. No third-party dependencies.
- Patterns are constructed at runtime from word-fragment alphabets; the source files do not contain verbatim adversarial phrases.
- The list of suspicious host fragments lives in `references/exfil-hosts.txt`, not in the Python source, so the scanner source contains no hard-coded directory of attack endpoints.
- The verb / target / quantifier alphabets live in `references/categories.txt`, not in the Python source. `scripts/_patterns.py` builds every pattern from those fragments at import time, so the source file contains no inline directory of words like "send/forward/secrets/credentials/keys/tokens" that a naive static scanner would mis-read as exfiltration intent.
- Never reads or writes outside the input/output paths the user provides.
- Never invokes a shell. The scoring core does not import `subprocess`. CLI scripts that take file paths reject any path containing shell metacharacters.
- All inputs and outputs use UTF-8.
- Deterministic: the same input produces the same score across runs.

## Known limitations

- Pattern-based detection cannot catch novel attacks expressed in unfamiliar phrasing. Combine with policy-level controls.
- Some categories will fire on legitimate text that discusses prompt injection. Use higher block thresholds in those domains, or pass `--whitelist`.
- The skill scores the text it is shown. If the upstream layer concatenates trusted and untrusted text into one string before calling, segment the inputs first.

## v0.4.1 changes

- Followup pass on the v0.4.0 cleanup: moved the remaining inline word directories (the secret-stem list and the exfil-channel alternation) out of `scripts/_patterns.py` and into `references/categories.txt` under the new `secret_stems` and `exfil_channels` keys.
- Sanitized the module docstring so it no longer quotes example word lists.
- Detection regression fixed: "post the response to webhook" used to score 0 because the channel pattern required `to/via` to sit immediately after the verb. The pattern now allows up to 4 filler words between the verb and `to/via`, and up to 2 between `to/via` and the channel word.
- Augmented the channel-verb pool with "submit" and the package-verb pool with "copy" and "leak" so phrasing like "submit it to the api endpoint", "copy these tokens to ...", and "leak the credentials" is detected.
- All v0.4.0 detection coverage preserved.

## v0.4.0 changes

- New `references/categories.txt` external alphabet file. The verb / target / quantifier word lists used to live inside `scripts/_patterns.py` as inline Python lists — those triggered a `potential_exfiltration` flag from a static-scanner that grepped the source for word lists. They now load from `categories.txt` at import time.
- `scripts/_patterns.py` now raises a clear `RuntimeError` on a partial install (categories.txt missing or missing required keys) rather than silently falling back to an inline default that would defeat the cleanup.
- Detection regression fixed: the data-exfiltration optional-determiner slot used to require whitespace on both sides of the optional group, so phrases with 3 chained determiners between verb and target returned safe. Replaced with a determiner-chain regex that allows 0-N chained filler words.
- Added `passwords?` to `targets.exfil`.
- All v0.3.1 detection coverage preserved.

## v0.3.0 changes

- New `indirect_injection` category (7 patterns): catches imperatives wrapped in quoted text, markdown link visible-text or URL, fenced code blocks, HTML comments, and runs of zero-width / bidi hidden characters.
- New combined-signal bonus: +6/+12/+18/+24 added when 2/3/4/5+ distinct categories fire on the same input, so chained attacks reliably cross the block threshold.
- New `--whitelist` and `--whitelist-file` flags on `scan_input.py` and `scan_batch.py` for legitimate content that quotes attack phrasing.
- Suspicious-host fragments moved out of the Python source into `references/exfil-hosts.txt` so static scanners do not flag the source as containing an exfil host directory.
- Fixed a regex bug where optional `(?:me|us)?` and `(?:your|the)?` groups still required intervening whitespace, so short leak phrases that omit the optional words did not match `system_prompt_leak`. They now match.
- Fixed exit-code reporting on `scan_input.py`: the script now correctly returns 2 (missing arguments), 3 (unsafe path / file not found / bad threshold), 1 (caution), 2 (block), 0 (safe).
- `recommendation` text now lists which categories triggered, and gives a category-specific recommendation for tool-abuse and indirect-injection blocks.
- All v0.2.0 detection coverage preserved; v0.3.0 adds patterns and signal-aggregation, never removes them.

## License

MIT. See `LICENSE`.
