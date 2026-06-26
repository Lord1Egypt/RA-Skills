## Description: <br>
HelloLeads (helloleads.io). Use this skill for ANY HelloLeads request - reading, creating, and updating data. Whenever a task involves HelloLeads, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect HelloLeads connector schemas, fetch visible web form definitions, and submit confirmed web form leads through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run credentialed HelloLeads connector actions, including submitting a web form lead. <br>
Mitigation: Use it only in a trusted ClawHub and OOMOL account context, inspect the live action schema, and confirm the exact write payload and effect before submission. <br>
Risk: Credentialed connector access can act through the currently connected OOMOL account and HelloLeads connection. <br>
Mitigation: Confirm the active account, connector target, and reason for the action before running commands that access or change HelloLeads data. <br>


## Reference(s): <br>
- [ClawHub HelloLeads release page](https://clawhub.ai/oomol/oo-helloleads) <br>
- [HelloLeads homepage](https://www.helloleads.io/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before request construction; command responses are JSON when run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
