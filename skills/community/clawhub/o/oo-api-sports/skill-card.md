## Description: <br>
API-SPORTS (api-sports.io) supports API-SPORTS requests that search and read sports data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query API-SPORTS football data, including fixtures, scores, events, lineups, statistics, standings, teams, players, injuries, and predictions, through OOMOL's oo CLI without handling raw API tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connecting API-SPORTS through OOMOL and permits an agent to run credential-backed oo connector commands for sports-data queries. <br>
Mitigation: Confirm the user is comfortable with the OOMOL connection before installation or use, and keep raw credentials outside the agent workflow. <br>
Risk: Optional CLI installation, login, billing, or app-connection steps could expose users to untrusted commands or pages if run unnecessarily or from the wrong source. <br>
Mitigation: Run setup steps only after matching command failures and use the documented OOMOL commands and pages. <br>


## Reference(s): <br>
- [API-SPORTS homepage](https://api-sports.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are expected as JSON with data and meta.executionId fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
