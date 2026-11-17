## Description:

Generates initiation-of-coverage or deep-dive equity research reports for supported A-share, Hong Kong, U.S., and Beijing Stock Exchange listed companies using Eastmoney data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial analysts use this skill to request comprehensive first-coverage or deep-dive research reports for supported listed companies. The skill returns a structured report response with generated content, attachment paths, and a share link when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the user's original prompt to Eastmoney's report-generation API.

Mitigation: Avoid prompts that contain confidential, personal, or restricted information, and disclose the external data transfer to users before operation.

Risk: The skill depends on EM_API_KEY for external service access.

Mitigation: Provide the key only through a controlled environment variable, restrict access to trusted runtimes, and rotate the key if exposure is suspected.

Risk: The skill saves generated PDF and Word report files locally.

Mitigation: Use a scoped output directory, review generated files before sharing, and remove files when they are no longer needed.

Risk: The security guidance flags unsafe redirects, unpinned dependencies, and under-scoped permissions as review concerns.

Mitigation: Prefer a reviewed release that disables unnecessary redirects, pins dependencies, and explicitly scopes network, environment-variable, and file-write permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/financial-ai-analyst/skills/initiation-of-coverage-or-deep-dive)
- [Eastmoney initial coverage API endpoint](https://ai-saas.eastmoney.com/proxy/app-robo-advisor-api/assistant/write/initial-coverage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown response with report text, local PDF/DOCX attachment paths, and a share URL; the helper script emits JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EM_API_KEY and may save generated report attachments under a local output directory.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
