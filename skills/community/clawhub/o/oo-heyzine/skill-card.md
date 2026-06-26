## Description: <br>
Heyzine helps agents manage Heyzine flipbooks and bookshelves through the OOMOL oo CLI for reading, updating, assigning, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to list and retrieve Heyzine flipbooks and bookshelves, then perform confirmed write or destructive maintenance through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Heyzine credentials through an OOMOL-connected account. <br>
Mitigation: Use the OOMOL connector flow so raw credentials are not handled by the agent, and reconnect only after an authentication or connection error. <br>
Risk: Write actions can change bookshelf assignments or social sharing metadata. <br>
Mitigation: Fetch the live action schema first, build an exact JSON payload, and confirm the payload and intended effect with the user before running the command. <br>
Risk: Destructive actions can delete flipbooks or remove bookshelf assignments. <br>
Mitigation: Require explicit user approval for the target resource and action before executing destructive commands. <br>


## Reference(s): <br>
- [ClawHub Heyzine Skill](https://clawhub.ai/oomol/oo-heyzine) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Heyzine](https://heyzine.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before building action payloads; command responses are JSON from the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
