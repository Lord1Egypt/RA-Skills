## Description: <br>
A/B testing and feature optimization for AI agents. Pick the best option automatically using Multi-Armed Bandits and Contextual Bandits (LinUCB). No data warehouse needed; works from request #1. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to choose among variants, run A/B tests without fixed sample sizes, optimize prompts or feature choices, and make context-aware selections using OraClaw bandit tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a separately configured OraClaw MCP server and external API key. <br>
Mitigation: Verify the OraClaw MCP server before installation and use an API key with appropriate limits. <br>
Risk: Optimization calls may incur paid usage and may include contextual business or user data. <br>
Mitigation: Monitor paid usage and avoid sending sensitive personal, regulated, or proprietary context unless OraClaw data handling and compliance terms have been confirmed. <br>


## Reference(s): <br>
- [OraClaw Bandit homepage](https://oraclaw.dev/bandit) <br>
- [ClawHub skill page](https://clawhub.ai/whatsonyourmind/oraclaw-bandit) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, text] <br>
**Output Format:** [Markdown guidance with JSON configuration and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ORACLAW_API_KEY and an OraClaw MCP server; paid optimization calls may apply.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
