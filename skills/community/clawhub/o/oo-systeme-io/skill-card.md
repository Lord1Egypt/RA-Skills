## Description: <br>
Systeme.io (systeme.io). Use this skill for ANY Systeme.io request - reading, creating, updating, and deleting data. Whenever a task involves Systeme.io, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and go-to-market teams use this skill to manage Systeme.io contacts, tags, webhooks, courses, enrollments, subscriptions, and custom fields through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Systeme.io account and may use sensitive account credentials through OOMOL-managed authentication. <br>
Mitigation: Install with normal caution and review requested tools, credentials, account connections, and install commands before first use. <br>
Risk: Write and destructive actions can change or remove Systeme.io contacts, tags, webhooks, enrollments, and subscriptions. <br>
Mitigation: Confirm the exact action, target, and payload with the user before running write actions, and require explicit approval before destructive actions. <br>
Risk: Live connector schemas may differ from assumptions in a user request. <br>
Mitigation: Fetch the action schema with `oo connector schema` before constructing payloads for connector runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-systeme-io) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Systeme.io homepage](https://systeme.io) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger live Systeme.io read, write, or destructive actions through the oo CLI when the user has connected credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
