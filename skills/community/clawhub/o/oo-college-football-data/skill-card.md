## Description: <br>
CollegeFootballData helps agents query college football account, conference, game, team, and venue data through the OOMOL CollegeFootballData connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when they want an agent to inspect CollegeFootballData connector schemas and run college football data lookups for account information, conferences, games and results, teams, and venues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence marks the release verdict as suspicious and notes full-access helper behavior that deserves manual review before installation. <br>
Mitigation: Install only if you trust the publisher, verify command targets before execution, and avoid full-access autoreview mode unless that authority is explicitly intended. <br>
Risk: The skill requires sensitive credentials through an OOMOL-connected CollegeFootballData account. <br>
Mitigation: Use the server-side credential flow, avoid exposing raw API keys, and run auth or connection setup only after a command fails for that reason. <br>


## Reference(s): <br>
- [CollegeFootballData ClawHub Skill Page](https://clawhub.ai/oomol/oo-college-football-data) <br>
- [CollegeFootballData Homepage](https://collegefootballdata.com/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector action responses are JSON objects containing data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
