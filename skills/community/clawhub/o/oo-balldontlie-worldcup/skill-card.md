## Description: <br>
BALLDONTLIE World Cup lets agents search and read FIFA World Cup data through the OOMOL balldontlie_worldcup connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve FIFA World Cup matches, teams, players, rosters, stadiums, standings, odds, injuries, and match statistics through an OOMOL-connected BALLDONTLIE account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on OOMOL account setup, provider connection, and possible billing state before data access works. <br>
Mitigation: Run login, connection, or billing setup only when a connector command fails for that specific reason. <br>
Risk: Connector action inputs may change over time. <br>
Mitigation: Inspect the live action schema before constructing and running each connector payload. <br>
Risk: The skill can retrieve betting-related World Cup odds data through the connected provider. <br>
Mitigation: Use it for explicit data lookup tasks and apply the user's own review before relying on returned odds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-balldontlie-worldcup) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [BALLDONTLIE World Cup homepage](https://fifa.balldontlie.io/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs the agent to inspect each action schema before running OOMOL connector commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
