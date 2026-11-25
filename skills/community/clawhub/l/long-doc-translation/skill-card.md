## Description:

Guides long-form translation projects from parsed source text through structured chunking, terminology management, quality checks, and delivery as a Chinese manuscript and self-contained HTML reader.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

External translators, editors, and researchers can use this skill to organize large scholarly translation projects, keep terminology consistent across sections, track uncertain passages, and prepare reviewable manuscript and reading files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment rates the release suspicious with medium confidence and reports an unpinned install command, a source/package mismatch, and partial inspection.

Mitigation: Pin the installer and reviewed skill revision, and compare packaged files with the reviewed source before installing.

Risk: Source documents may be sent to an external parsing service.

Mitigation: Check the parsing destination and confirm you are authorized to share the documents; use an approved local parser for sensitive material.

Risk: Some translation quality checks can skip comparisons or report a passing result when a check did not run.

Mitigation: Review skipped-check notices and manually check segment coverage, terminology consistency, and the final output.

## Reference(s):

- [ClawHub release](https://clawhub.ai/huhoo/skills/long-doc-translation)
- [English README](README.en.md)
- [Translation pitfalls](references/pitfalls.md)
- [Quality assurance checklist](references/qa-checklist.md)
- [Parallel translation guidance](references/parallel-translation.md)
- [Reader build guidance](references/reader-build.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Translation guidance]

**Output Format:** [Chinese translation drafts and deliverables in Markdown and self-contained HTML, with glossary and review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Organized by source structure; includes terminology tracking and uncertainty annotations for human review.]

## Skill Version(s):

1.3.19 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
