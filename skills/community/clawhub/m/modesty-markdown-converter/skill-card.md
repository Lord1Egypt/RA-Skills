## Description:

Convert documents and files to Markdown using markitdown. Use when converting PDF, Word (.docx), PowerPoint (.pptx), Excel (.xlsx, .xls), HTML, CSV, JSON, XML, images (with EXIF/OCR), audio (with transcription), ZIP archives, YouTube URLs, or EPubs to Markdown format for LLM processing or text analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert documents, data files, media, archives, and web sources into Markdown for LLM processing or text analysis. For complex documents, the skill also describes an optional SkillBoss API Hub workflow for remote document extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local conversion runs unpinned third-party markitdown code via uvx, so behavior can change across runs.

Mitigation: Pin and review the markitdown version before deployment, and review generated Markdown before relying on it.

Risk: The optional SkillBoss API Hub path can send submitted document URLs, metadata, or content to SkillBoss when SKILLBOSS_API_KEY is set.

Mitigation: Use the remote API path only for documents approved for SkillBoss processing, and leave SKILLBOSS_API_KEY unset for local-only conversion.

Risk: The --use-plugins option enables third-party plugins that may expand the skill's trust boundary.

Mitigation: Avoid --use-plugins unless each plugin is vetted and approved for the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/modestyrichards/skills/modesty-markdown-converter)
- [SkillBoss setup guide](https://skillboss.co/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with shell commands and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output preserves document structure such as headings, tables, lists, and links when supported by the converter.]

## Skill Version(s):

1.0.2 (source: server release evidence, created 2026-04-15T05:17:50Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
