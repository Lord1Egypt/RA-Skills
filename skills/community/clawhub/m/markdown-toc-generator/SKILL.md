---
name: markdown-toc-generator
description: >
  Insert or refresh a table of contents for Markdown headings. Use when a
  long doc needs an up-to-date TOC under a marker comment.
metadata: {"clawdbot":{"emoji":"📑","requires":{"bins":["python3"]}}}
---

# Markdown TOC Generator

## Purpose / Overview
Builds a nested TOC from `#`–`######` headings.

## When to Use
- README or design doc grew long
- User asks to "update the TOC"

## Usage / Instructions
1. Take the Markdown path from the user.
2. Run `python3 scripts/make_toc.py <path>`.
3. Show the TOC; write back only if the user confirms.

## Examples
```bash
python3 scripts/make_toc.py ./README.md
```

## Requirements / Dependencies
python3 (stdlib).

## Limitations / Caveats
Skips fenced code blocks when detecting headings (best-effort).

## Security / Permissions
Reads (and optionally writes) only the path provided. No network.

## Description

Insert or refresh a table of contents for Markdown headings.

## License or terms

Business

## Use case

For users and teams who want a concise assistant for: Insert or refresh a table of contents for Markdown headings.

## Risks and mitigations

## References

- CommonMark specification: https://commonmark.org/

## Ethical considerations

Illegal use of this skill is not allowed. The publisher will not be accountable for outcomes arising from unlawful use under country or international law. Prohibited examples include breaking into accounts without authorization, deploying ransomware, and trafficking in stolen personal data. Misuse against third-party systems without authorization is illegal.
