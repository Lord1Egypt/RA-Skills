## Description:

Collects and reports Xiaohongshu profile, note, search, and trend data for marketing analysis, while the reviewed artifact currently produces demo Markdown reports rather than verified live data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoheizp](https://clawhub.ai/user/xiaoheizp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and marketing teams use this skill to prepare Xiaohongshu profile, note, search, and trend reports for content and competitive analysis. Review security guidance before providing credentials because the inspected artifact is reported to generate demo outputs rather than authenticated live data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for a live Xiaohongshu session cookie while release security evidence says the inspected code does not use the credential.

Mitigation: Do not provide a Xiaohongshu cookie until the skill clearly implements authenticated scraping, documents credential handling, and protects the credential appropriately.

Risk: The skill advertises real Xiaohongshu scraping while security evidence says the current artifact should be expected to produce demo reports.

Mitigation: Treat generated reports as demo outputs unless the installed artifact is updated and independently verified against live data sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaoheizp/skills/ke-xiaohongshu-data)
- [Publisher Profile](https://clawhub.ai/user/xiaoheizp)
- [Artifact Skill Instructions](artifact/SKILL.md)
- [Example Notes Export](artifact/xiaohongshu-notes.md)
- [Example Analysis Report](artifact/xiaohongshu-report.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires review before credentialed use; release evidence identifies XIAOHONGSHU_COOKIE as the primary environment variable.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
