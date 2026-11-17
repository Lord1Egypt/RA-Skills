## Description:

Fact-checking tool for verifying the factual accuracy of input statements or suspicious claims, identifying rumors, and assessing content credibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencentnewsteam](https://clawhub.ai/user/tencentnewsteam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check factual claims, suspicious information, rumors, and short statements with Tencent News Jiaozhen CLI results. It guides environment setup, API-key validation, CLI command selection, and preserves the returned fact-check markdown as the response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct users to execute remote installer or update commands for an external Tencent CLI.

Mitigation: Verify the publisher, installer source, and binary integrity before running installation or update commands.

Risk: The installation guide includes OS security-warning bypass steps for the external CLI.

Mitigation: Do not bypass operating-system warnings unless the Tencent distribution channel and downloaded artifact have been independently verified.

Risk: The skill requires local API-key configuration for the external CLI.

Mitigation: Enter keys only in the local terminal, avoid sharing keys with the agent, and clear or rotate keys if exposure is suspected.

## Reference(s):

- [Jiaozhen Factcheck Skill Page](https://clawhub.ai/tencentnewsteam/skills/jiaozhen-factcheck)
- [TencentNewsTeam Publisher Profile](https://clawhub.ai/user/tencentnewsteam)
- [API Key Setup Guide](references/env-setup-guide.md)
- [Installation Guide](references/installation-guide.md)
- [Update Guide](references/update-guide.md)
- [API Key Exchange Page](https://news.qq.com/exchange?scene=appkey)
- [Jiaozhen AI Fact-Check Web Entry](https://view.inews.qq.com/ai/agent/UTR2025041800262600?no-redirect=1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with CLI output and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI status JSON during setup and complete fact-check markdown from the external CLI during verification.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
