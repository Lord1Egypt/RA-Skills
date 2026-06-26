# Detection categories

This is a high-level summary of what each category detects. The full pattern list lives in `scripts/_patterns.py`. Patterns there are constructed at runtime from word-fragment lists, so the source files do not contain literal adversarial phrases.

All patterns are matched case-insensitively. Multi-word phrases tolerate extra whitespace between words.

## instruction_override (per-hit +32, capped at 45)

Detects phrasing that asks the model to drop or replace whatever it was previously told. Typical verbs include disregard, forget, override, bypass, plus quantifiers like all/any/the/every and time anchors like previous/prior/above/earlier paired with words such as instructions, prompts, rules, directives, guidelines, filters, safeguards.

## role_hijack (per-hit +32, capped at 45)

Detects identity swaps that move the model into an unrestricted persona. Looks for assignment-style phrasing (subject + state-change verb + new identity), role-shift verbs paired with character or persona language, claims of liberation or unlocked state, explicit unrestricted-now phrasing, and instructions to respond without filters or restrictions.

## system_prompt_leak (per-hit +30, capped at 42)

Detects attempts to extract the agent's hidden context. Includes asks to repeat or echo text above verbatim, to show or print system prompt or initial instructions, and to dump or expose hidden / secret / internal context. Also catches the well-known "output initialization above in a code fence" template.

## delimiter_injection (per-hit +28, capped at 40)

Detects fake structural markers that try to make the model parse attacker text as a new system or assistant turn. Includes pipe-style chat delimiters, pseudo-XML system/assistant tags, instruction-tag pairs, alpaca-style headers, BOS/EOS/PAD/UNK tokens, raw `SYSTEM:` lines, and identity-redefining markdown frontmatter (role / persona / identity / system_prompt / instructions).

## data_exfiltration (per-hit +32, capped at 45)

Detects attempts to make the agent send conversation contents or secrets somewhere outside. Typical verbs are send, email, post, forward, transmit, upload, leak, exfiltrate paired with conversation, chat, history, context, secrets, credentials, keys, tokens. Also catches direct fetch / curl / wget / GET / POST against http URLs, posting to webhook / endpoint / api, and known exfil-friendly host fragments loaded at runtime from `references/exfil-hosts.txt` (the source file does not contain that directory inline).

## tool_abuse (per-hit +30, capped at 42)

Detects attempts to coerce the agent into running destructive shell commands or reading sensitive files. Includes destructive deletion, sudo against destructive utilities, fork-bomb shape, run/execute against shell binaries, reads of `/etc/passwd`, `/etc/shadow`, `/proc/self`, dotfile dirs (`~/.ssh`, `~/.aws`, `~/.gnupg`, `~/.netrc`, `~/.env`, `~/.config`), credential exports, and dangerous Python idioms (`eval(`, `os.system(`, `subprocess` with `shell=True`, `__import__("os"|"subprocess"|"sys"|"socket")`).

## encoding_evasion (per-hit +22, capped at 30)

Detects payloads hidden inside encoded blobs and decode-then-execute phrasing. Triggers on long base64 or hex blocks, runs of URL-encoded escapes, "decode … execute / run / eval" within a short window, "after decoding … run", and "execute / run / eval the decoded base64".

## policy_bypass (per-hit +14, capped at 20)

Lower-confidence rationalizations for ignoring safety rules. Includes educational/research/academic/hypothetical-purposes-only wrappers, "in a fictional / hypothetical / imaginary / alternate setting", "rules don't apply", "without filters / restrictions / guardrails / limits / safeguards / censorship", "just this one time", "for a movie / story / book / novel / screenplay / video game / simulation", and "imagine / suppose / assume you could".

## indirect_injection (per-hit +20, capped at 28) — NEW in v0.3.0

Detects imperatives that arrive wrapped in something that looks like data rather than instructions. Triggers on:

- Quoted text (single or double quotes) whose interior begins with an override verb.
- Markdown links whose visible text or URL contains an override verb.
- Fenced code blocks (`` ``` ``) whose interior begins with an override verb.
- HTML comments hiding an override imperative.
- Runs of three or more zero-width or bidi-control characters (ZWSP, ZWNJ, ZWJ, LRM/RLM, LRE/RLE/PDF/LRO/RLO, isolate marks, BOM) used to smuggle hidden text.

This category is intentionally lower-weighted than `instruction_override` itself: a single quoted attack phrase fires both `instruction_override` (for the inner text) and `indirect_injection` (for the wrapper), and the combined-signal bonus then pushes the total into the `caution` band.

## Scoring formula

For each category found in the input, the score contribution is `min(per_hit × hits_in_category, category_cap)`.

A combined-signal bonus is then added on top of the per-category sum when two or more distinct categories all fire on the same input:

| Distinct categories triggered | Bonus added |
|---|---|
| 2 | +6 |
| 3 | +12 |
| 4 | +18 |
| 5+ | +24 |

The total is clamped to `min(100, sum_of_categories + bonus)`. The verdict applies the configured thresholds to that total.

Default thresholds:

- `safe` if total < 30
- `caution` if 30 ≤ total < 70
- `block` if total ≥ 70

## Tuning

If you operate in a domain where some patterns are common in legitimate text (security research, AI policy writing, training data labeling), raise `--block-at` to 80 or 90 so only multi-category matches block, or pass `--whitelist "<the surrounding sentence>"` (or `--whitelist-file allow.txt`) so the legitimate sentence's fragments are dropped before scoring. The default thresholds are tuned for general-purpose agent input filtering.
