## Description: <br>
The Odds API (the-odds-api.com) skill helps agents search and read sports odds, scores, events, participants, and market data through the OOMOL `oo` CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to an OOMOL-connected The Odds API account for sports odds, scores, events, participants, and market lookup tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a connected OOMOL account for The Odds API access. <br>
Mitigation: Install only if you trust OOMOL and want the agent to use that connected account. <br>
Risk: Live odds queries may consume The Odds API account quota or credits. <br>
Mitigation: Monitor API usage and stop retrying when billing or insufficient-credit errors occur. <br>
Risk: First-time setup may require installing the oo CLI from an external install command. <br>
Mitigation: Review the oo CLI installation command before running it. <br>


## Reference(s): <br>
- [The Odds API homepage](https://the-odds-api.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-the-odds-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses include data and a meta.executionId when actions run successfully.] <br>

## Skill Version(s): <br>
1.0.1 (source: artifact frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
