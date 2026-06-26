## Description: <br>
Operate Rollbar through an OOMOL-connected account for reading, creating, and updating Rollbar data via the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and support teams use this skill to inspect Rollbar projects, items, occurrences, deploys, environments, and item occurrence lists, and to run approved connector actions against a connected Rollbar account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Rollbar credentials through the OOMOL connector. <br>
Mitigation: Install only when the user trusts OOMOL as the intermediary for the Rollbar connection. <br>
Risk: Read actions can expose sensitive Rollbar project, item, occurrence, deploy, and environment data. <br>
Mitigation: Treat read results as sensitive operational data and share them only with authorized recipients. <br>
Risk: Connector actions tagged as write or destructive may change or remove Rollbar data. <br>
Mitigation: Inspect the live action schema and require explicit user confirmation of the target, payload, and expected effect before running those actions. <br>


## Reference(s): <br>
- [ClawHub Rollbar Skill](https://clawhub.ai/oomol/oo-rollbar) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [Rollbar Homepage](https://rollbar.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses include data and execution metadata when run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
