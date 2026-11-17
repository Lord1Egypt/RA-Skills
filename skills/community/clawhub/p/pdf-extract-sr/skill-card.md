## Description:

Extract clean readable text from PDF files into agent-ready markdown. Multi-page, tables, headers. No external services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to extract readable text, page content, metadata, headings, and markdown from local PDF files for downstream analysis or documentation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read any local PDF path the agent is asked to process.

Mitigation: Only provide intended PDF paths and avoid running it over directories or files outside the task scope.

Risk: Extracted PDF contents may be exposed to the active agent conversation.

Mitigation: Use caution with sensitive PDFs and redact or avoid documents that should not enter the agent context.

Risk: The fallback path may invoke local PDF tooling.

Mitigation: Review the local environment and installed PDF tools before deployment in controlled systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/pdf-extract-sr)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown and JavaScript usage examples with extracted text or structured result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local PDF processing; structured extraction can include page text, metadata, headings, method, and per-file batch results.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
