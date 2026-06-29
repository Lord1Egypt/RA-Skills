## Description: <br>
football-data.org helps an agent query competitions, teams, standings, matches, and individual match details through OOMOL's football_data connector instead of calling the football-data.org API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve read-only football-data.org information through an OOMOL-connected account, including competition lists, team lists, standings, match lists, and individual match records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the oo CLI can modify the user's local command-line environment. <br>
Mitigation: Review the OOMOL installer or install guide before running it on a new machine. <br>
Risk: football-data.org access is mediated through an OOMOL server-side connection rather than direct local API credentials. <br>
Mitigation: Use an OOMOL account and football-data.org connection appropriate for the user's data-access and billing expectations. <br>
Risk: Connector action schemas may change over time, causing malformed payloads or unexpected query results. <br>
Mitigation: Fetch the live connector schema before building payloads and keep actions limited to the documented read-only get and list workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-football-data) <br>
- [football-data.org homepage](https://www.football-data.org/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live connector schema before running connector actions; connector responses are JSON from the oo CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
