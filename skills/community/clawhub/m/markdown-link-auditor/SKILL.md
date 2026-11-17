---
name: markdown-link-auditor
description: >
  Audit Markdown for link issues: empty labels, duplicate URLs, raw URLs, and
  suspicious schemes. Use when cleaning README or docs before publish.
metadata: {"clawdbot":{"emoji":"🔗","requires":{"bins":[]}}}
---

# Markdown Link Auditor

## Purpose / Overview
Scan pasted Markdown for link hygiene problems and produce a fix list. This
skill inspects text structure; it does not fetch URLs unless the user later
asks for live checks.

## When to Use
- README cleanup
- Docs migration
- Preparing a release announcement page

## Usage / Instructions
1. Ask for the Markdown content (or a file excerpt).
2. Extract inline links `[text](url)` and image links `![alt](url)`.
3. Also note bare URLs and reference-style definitions.
4. Report findings in categories:
   - empty or whitespace-only link text
   - empty or `#` placeholders
   - duplicate URLs with different labels
   - duplicate labels pointing at different URLs
   - `javascript:` or other odd schemes
   - images missing alt text
5. For each finding: line quote (short), issue, suggested rewrite.
6. Give a count summary at the top (files not needed if single paste).
7. Prefer preserving author wording when fixing labels.
8. Do not rewrite unrelated prose.
9. If the user asks to check HTTP status, warn that needs network and only
   proceed with explicit approval URL-by-URL.
10. Finish with a prioritized checklist (blockers vs nice-to-have).
11. Keep answers structured with short headings so the user can skim.
12. If information is missing, ask at most two clarifying questions before guessing.
13. Prefer concrete commands or checklists the user can copy.
14. Call out assumptions explicitly when the environment is unknown.
15. Refuse to invent tool output you did not see; ask for a fresh paste instead.
16. When offering optional follow-ups, keep them clearly optional.
17. Stay within this skill's scope; suggest a different task type if the request drifts.
18. End with a brief "done when" criterion so the user knows success.


## Examples
README with three `(#)` placeholders and one image without alt
→ list placeholders as blockers; alt as medium.

## Requirements / Dependencies
None for static audit.

## Limitations / Caveats
Cannot know if a relative link exists on disk without the full tree.
Live link checking is out of default scope.

## Security / Permissions
Do not fetch links by default. Do not open `javascript:` or data URLs.

## Attribution / License
MIT-0

## Description

Audit Markdown for link issues: empty labels, duplicate URLs, raw URLs, and suspicious schemes.

## License or terms

MIT-0

## Use case

For users and teams who want a concise assistant for: Audit Markdown for link issues: empty labels, duplicate URLs, raw URLs, and suspicious schemes.

## Risks and mitigations

## References

- MDN HTTP response status codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- CommonMark specification: https://commonmark.org/

## Ethical considerations

Any illegal use is prohibited. Usage that contravenes the law of the country of operation or international law is not acceptable. The publisher will not be accountable for illegal use. Do not apply this skill to money laundering support, sanctions evasion, or unauthorized surveillance. Do not use this skill to bypass access controls you are not entitled to.
