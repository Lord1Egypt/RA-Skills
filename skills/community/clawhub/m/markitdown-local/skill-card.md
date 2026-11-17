## Description:

Convert local or uploaded documents to AI-friendly Markdown with Microsoft MarkItDown, preserving originals and reporting conversion gaps. Use when asked to convert files to Markdown; this does not upload, summarize, or sanitize them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huipan1973](https://clawhub.ai/user/huipan1973)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use the skill to convert user-provided local documents into Markdown for downstream reading or analysis. It also reports conversion failures and extraction limits so users can check results against the original files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Converted Markdown may retain sensitive information and source metadata; conversion does not sanitize content.

Mitigation: Screen newly uploaded raw files before conversion and apply the upload preflight to converted Markdown and its metadata before sending it to a model or service.

Risk: Extraction may omit visual layout or content from scanned pages, images, or audio.

Mitigation: Review the conversion report and compare the output with the original when completeness matters; report unsupported files and known extraction gaps.

## Reference(s):

- [Microsoft MarkItDown project](https://github.com/microsoft/markitdown)
- [ClawHub skill release](https://clawhub.ai/huipan1973/skills/markitdown-local)

## Skill Output:

**Output Type(s):** [Files, Markdown, Guidance]

**Output Format:** [Markdown conversion files with concise status and extraction-limit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps source files unchanged; writes distinct Markdown outputs and reports unsupported files or extraction gaps.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
