## Description:

Generates Chinese-language tracking reports for industries or individual stocks using Eastmoney data, including periodic reports, research reports, and structured tracking analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[financial-ai-analyst](https://clawhub.ai/user/financial-ai-analyst)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial analysts use this skill to request Chinese-language industry or stock tracking reports from natural-language prompts. It returns report text, local attachment paths, and a share link when the remote service provides them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Report prompts and API-key-authenticated requests are sent to Eastmoney's remote report service.

Mitigation: Avoid confidential strategy, account, or personal information in prompts unless that disclosure is acceptable.

Risk: Generated DOCX/PDF report attachments are saved locally without a stated cleanup policy.

Mitigation: Periodically review retained files and delete generated reports that are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/financial-ai-analyst/skills/industry-stock-tracker)
- [Eastmoney report service endpoint](https://ai-saas.eastmoney.com/proxy/app-robo-advisor-api/assistant/write/tracking/report)

## Skill Output:

**Output Type(s):** [text, markdown, files]

**Output Format:** [Chinese Markdown report text with PDF/DOCX attachment paths and a share link; the helper script emits JSON for the agent to format.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EM_API_KEY and may save generated PDF/DOCX files locally.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
