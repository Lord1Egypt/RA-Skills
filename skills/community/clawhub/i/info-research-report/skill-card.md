## Description:

Automates information research workflows by gathering search results, summarizing sources, generating public-sector-style DOCX research reports, and sending them by email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaferliu](https://clawhub.ai/user/zaferliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research staff use this skill to turn browser-gathered public web sources or a results.json file into a structured Chinese DOCX research report and email it to a specified recipient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input data may contain arbitrary URLs that the skill fetches and summarizes.

Mitigation: Use trusted results.json files, avoid internal or private URLs, and prefer --no-fetch for sensitive work.

Risk: Webpage content, prompts, summaries, generated reports, or attachments may be processed by configured third-party AI and email services.

Mitigation: Confirm third-party privacy and compliance requirements, use dedicated API keys, and review the DOCX before sending it externally.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zaferliu/skills/info-research-report)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Configuration instructions]

**Output Format:** [DOCX report file with terminal status text and generated email content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can fetch page content unless --no-fetch is used; generated reports should be reviewed before external sharing.]

## Skill Version(s):

1.0.6 (source: server release metadata; package.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
