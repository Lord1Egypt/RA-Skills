## Description: <br>
Rentman support for searching and reading data through Rentman requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search and read Rentman contacts, contact persons, equipment, and projects through their connected OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read Rentman business data through the user's connected OOMOL account. <br>
Mitigation: Install and use it only when the user intends the agent to access Rentman data, and scope requests to the needed records. <br>
Risk: Future connector actions that create, update, delete, or overwrite data could change Rentman state. <br>
Mitigation: Require explicit user confirmation of the exact action, target, payload, and expected effect before running any write or destructive action. <br>
Risk: First-time setup may require installing the oo CLI and signing in to OOMOL. <br>
Mitigation: Run setup steps only after an auth, connection, or missing-command failure, and avoid exposing raw credentials in prompts or logs. <br>


## Reference(s): <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Rentman homepage](https://rentman.io) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-rentman) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before action calls; action responses are JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
