## Description: <br>
Quo (OpenPhone) connector skill that helps an agent inspect live schemas and use the OOMOL oo CLI to read, create, update, delete, and send messages in a connected Quo workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and support teams use this skill to manage Quo (OpenPhone) contacts, messages, phone numbers, users, and outbound text messages from an OOMOL-connected workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change Quo workspace data by creating or updating contacts and sending text messages. <br>
Mitigation: Inspect the live connector schema, review the exact JSON payload and expected effect, and get explicit user confirmation before running write or messaging actions. <br>
Risk: The skill can delete contacts from the connected Quo workspace. <br>
Mitigation: Confirm the target contact and obtain explicit approval before running destructive actions. <br>
Risk: The skill depends on the OOMOL oo CLI and an active Quo/OpenPhone connection. <br>
Mitigation: Install and authenticate the CLI only when required, and review the official installer or install guide before setup. <br>


## Reference(s): <br>
- [Quo (OpenPhone) homepage](https://www.quo.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub listing](https://clawhub.ai/oomol/oo-quo) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live connector schema inspection before action execution; write, messaging, and destructive actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
