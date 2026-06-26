## Description: <br>
Jarvis Stock Monitor monitors configured stocks, ETFs, and gold positions with price, cost-basis, volume, technical-indicator, gap, and trailing-stop alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[15910701838](https://clawhub.ai/user/15910701838) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users configure watchlists and cost bases so an agent can monitor Chinese A-shares, ETFs, and gold, then surface tiered alerts and analysis-style messages. The skill is intended as monitoring and reference material, not professional investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured watchlists and cost bases can reveal portfolio-like financial interests during market-data polling. <br>
Mitigation: Review the configured holdings before use and only run continuous monitoring when those local details are acceptable for the selected data sources. <br>
Risk: The skill produces advisory-style buy, hold, sell, and risk messages that may be incomplete or misleading. <br>
Mitigation: Treat generated alerts and analysis as non-professional reference material and confirm decisions with independent financial review. <br>
Risk: The daemon runs background polling until stopped. <br>
Mitigation: Start the daemon only when continuous monitoring is desired and use the provided control script to check status, view logs, or stop it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/15910701838/jarvis-stock-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and alert message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces monitoring alerts and analysis-style summaries from user-configured market watchlists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
