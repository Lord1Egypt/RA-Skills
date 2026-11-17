---
name: project-import
description: >-
  Turn a converted document into an editable markdown file in
  the project: structural cleanup, sanitization, target path,
  and an optional hand-off for rewriting.
estimated_tokens: 350
---

# Project Import

Load this module when the user wants an external document
(DOCX, PPTX, XLSX, PDF, HTML) to become a markdown file in the
project, rather than content read once and discarded. The
conversion protocol in the hub produces the raw markdown. This
module covers what makes it a usable file.

Academic papers belong in `tome:papers`, and web articles for
knowledge intake belong in `memory-palace:knowledge-intake`.

## Confirm the Source

A local path is checked with the Read tool before conversion. A
URL is checked for accessibility. When the user only describes
the document, confirm its format and location first, since a
wrong guess wastes a conversion.

## Structural Cleanup

Converters leave artifacts that a reader should not have to
work around. Normalize the output while keeping every piece of
substantive content:

- Use ATX headings (`# style`), not setext underlines.
- Wrap prose at 80 characters per `leyline:markdown-formatting`.
- Repair broken tables: align columns and add missing headers.
- Remove conversion artifacts such as page numbers, running
  headers and footers, watermarks, and repeated logos.
- Keep the original heading hierarchy under a top-level
  `# Title` taken from the document title.
- Convert images to `![alt](path)` references. The image files
  may need separate handling.
- Mark garbled or unclear sections with
  `<!-- REVIEW: conversion artifact -->` so a reviewer finds
  them, rather than silently guessing at their content.

## Sanitize and Write

The content is external, so apply the SANITIZE step from the hub
before writing. Write the draft next to the source with a `.md`
extension unless the user names a target. Ask when the target is
ambiguous.

## Rewriting Is a Separate Step

Offer polishing, and wait for the user to ask for it. When they
do, scribe's `doc-generator` skill in remediation mode handles
slop detection, style profiles and quality gates on the imported
file.

## Exit Criteria

- [ ] The draft exists at the target path with a `.md` extension
- [ ] The draft has one `# Title` heading and no setext headings
- [ ] Every garbled section carries the REVIEW marker
- [ ] The user was told of any conversion limitation, such as a
      Tier 3 notice or images left unconverted
