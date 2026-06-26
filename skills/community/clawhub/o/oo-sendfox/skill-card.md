## Description: <br>
SendFox helps agents read, create, update, and delete SendFox contact and contact-list data through the OOMOL oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate SendFox accounts from an agent, including contact lookup, list management, contact creation, updates, unsubscribes, and soft-delete workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected SendFox account and may use sensitive credentials through OOMOL-managed connector access. <br>
Mitigation: Grant only the account access needed for the intended task and avoid adding extra tools or credentials beyond the documented oo CLI connector flow. <br>
Risk: Write and destructive actions can change SendFox contacts, list memberships, unsubscribe status, or soft-delete contacts and lists. <br>
Mitigation: Confirm the exact target, payload, and expected effect with the user before running any action marked write or destructive. <br>
Risk: Connector schemas and account connection state can change outside the skill text. <br>
Mitigation: Fetch the live action schema before building payloads and use first-time setup steps only after an authentication, connection, scope, or billing error occurs. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/oomol/oo-sendfox) <br>
- [SendFox homepage](https://sendfox.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May issue oo CLI commands that return JSON responses from SendFox connector actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
