## Description:

Generates industry research reports for recognizable industries or market sectors using the Eastmoney data service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to turn an industry-focused request into a structured research report with a title, summary text, PDF and DOCX attachments, and a share link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned Python dependency.

Mitigation: Install in an isolated virtual environment and pin dependency versions before production use.

Risk: The skill downloads and stores remote PDF and DOCX report files.

Mitigation: Set INDUSTRY_RESEARCH_REPORT_OUTPUT_DIR to a controlled writable directory and treat generated attachments as untrusted until reviewed.

Risk: The skill uses an EM_API_KEY for a remote service call.

Mitigation: Use a scoped key, keep it in a trusted environment, and avoid logging or sharing the key.

Risk: The service may return a share link to remote content.

Mitigation: Open share links only in trusted network environments and verify the destination before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/financial-ai-analyst/skills/industry-research-report)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown response with generated report excerpt, local PDF and DOCX file paths, and a share URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EM_API_KEY and may write report files to INDUSTRY_RESEARCH_REPORT_OUTPUT_DIR or a default local output directory.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
