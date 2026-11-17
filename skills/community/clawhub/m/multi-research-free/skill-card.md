## Description:

Prompts an agent to produce multi-perspective A-share investment research analysis across fundamentals, technical signals, news sentiment, and risk factors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and investment research teams use this skill to prompt an agent to analyze A-share stocks from fundamental, technical, news sentiment, and risk perspectives, then produce research summaries, scores, alerts, and decision-support guidance. Use it as informational research rather than as a trading authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finance-analysis output may be mistaken for trading authority or buy/sell advice.

Mitigation: Use the skill only for informational research, independently verify market data, and require human review before investment decisions.

Risk: The skill asks for broad agent tools and API-key use.

Mitigation: Use secure secret management, avoid storing API keys in prompts or files, and require explicit confirmation before commands, package installs, or file writes.

Risk: The security scan flags unsupported claims about security controls and investment-analysis capability.

Mitigation: Treat artifact security and performance claims as unverified; review and scan the skill before installation or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/multi-research-free)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with structured JSON examples, code snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require external market data or API keys; investment conclusions require independent verification and human review.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
