# Security review notes

## What this skill is

`openclaw-prompt-shield` is a **defender-side input-hardening scanner** for
OpenClaw agents. It looks at user-submitted text *before* the agent
processes it and returns a risk score, a verdict, and a sanitized version.
It does not call any LLM, classifier API, or remote service. It does not
make network requests. It does not read or write any path the caller has
not explicitly provided.

The detection engine is pure-Python regex matching over standard library.

## Why the static-scanner flag may appear

A naive static-scanner that greps the skill bundle for a frequency of
words like `send / forward / webhook / secrets / credentials / keys /
tokens` will see a high frequency of those words in
`references/categories.txt` and `references/exfil-hosts.txt`. Those files
are not attacker intent. They are the **detection-rule alphabets** the
scanner uses to recognise such phrasing in incoming user text and flag it
as risky.

In other words: if this skill did not contain those words, it could not
do its job. A virus scanner is allowed to ship a list of virus
signatures; an input-hardening skill is allowed to ship a list of
attack-signal fragments.

The LLM-based scanner included with ClawHub correctly recognises this
pattern and marks v0.4.x as `benign (clean)` with the summary:

> "This appears to be a local prompt-injection scanner with expected
> file I/O and no supported evidence of real network exfiltration in
> the provided artifacts."

## Verifiable safety claims

- `scripts/_core.py` and `scripts/_patterns.py` do **not** import
  `subprocess`, `socket`, `urllib`, `requests`, `http`, or any other
  network module.
- `scripts/scan_input.py`, `scripts/scan_batch.py`, and
  `scripts/sanitize_input.py` only use `argparse`, `json`, `pathlib`,
  `re`, `sys` from the standard library.
- All file-reading paths are validated against a whitelist character set
  (`_\\.\\-\\+ @=:%,()'\\[\\]`) and the script refuses any path containing
  shell metacharacters such as `;`, `|`, `&`, `>`, `<`, `$`, `` ` ``.
- The `_patterns.py` module raises a clear `RuntimeError` on a partial
  install (when `references/categories.txt` is missing or incomplete) so
  the failure mode is immediate and visible, rather than silently
  falling back to an inline word table.
- No part of this skill calls `eval`, `exec`, `compile`, `pickle.loads`,
  or any other deserialisation primitive on user-controlled input.
- All file outputs (sanitized text, batch reports, safe-subset JSONL)
  go to caller-supplied paths only.

## Known false-positive: `suspicious.potential_exfiltration`

ClawHub's static scanner currently emits
`suspicious.potential_exfiltration` for this skill on every published
version because of the keyword frequency described above. This is a
known false-positive and is documented here so reviewers do not need to
re-derive the analysis. To install the skill, use:

```bash
clawhub install openclaw-prompt-shield --force
```

or, when reviewing source, focus on `scripts/_core.py` and
`scripts/_patterns.py` for the actual runtime behaviour, and treat the
`references/*.txt` files as **defender-side rule data** rather than
attacker intent.

## Reporting real concerns

If a real issue is found - for example, a regex that crashes the
interpreter on a specific input, a path-validation bypass, or a way to
make the scanner approve an attack it should block - please open an
issue or contact the maintainer through the ClawHub plugin page:
<https://clawhub.ai/gopendrasharma89-tech/openclaw-prompt-shield>.
