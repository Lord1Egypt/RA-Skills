## Description: <br>
Weatherbit enables an agent to retrieve current, daily, and hourly Weatherbit weather data through the OOMOL oo CLI with server-side credential injection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to retrieve Weatherbit current observations and forecasts through an OOMOL-connected account without handling raw Weatherbit tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Weatherbit account and may depend on sensitive account credentials managed outside the local workspace. <br>
Mitigation: Install and use it only when Weatherbit access through OOMOL is intended, and review any one-time authentication or connection step before approving it. <br>
Risk: Connector setup or billing errors can block weather requests or prompt additional account actions. <br>
Mitigation: Treat setup, connection, and billing steps as one-time account operations and perform them only after a command fails with the matching error. <br>


## Reference(s): <br>
- [ClawHub Weatherbit Skill](https://clawhub.ai/oomol/oo-weatherbit) <br>
- [Weatherbit Homepage](https://www.weatherbit.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before execution and returns Weatherbit responses as JSON through the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
