## Description: <br>
Vapi (vapi.ai). Use this skill for ANY Vapi request: reading, creating, updating, and deleting data through the OOMOL oo CLI instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Vapi assistants, calls, chats, phone numbers, sessions, evals, scorecards, monitoring policies, analytics, provider resources, tools, and files through an OOMOL-connected Vapi account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Vapi account through OOMOL and can operate on sensitive account data. <br>
Mitigation: Install only when OOMOL is an acceptable connector for the Vapi account and keep account connection scopes under review. <br>
Risk: Optional first-time setup includes a pipe-to-shell installer pattern. <br>
Mitigation: Prefer the official install guide or verify the installer source before running setup commands. <br>
Risk: Write and destructive actions can change or delete Vapi resources. <br>
Mitigation: Fetch the live action schema, review the exact payload and target, and obtain explicit approval before write or destructive actions. <br>


## Reference(s): <br>
- [Vapi homepage](https://vapi.ai) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-vapi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before executing actions and returns OOMOL connector responses as JSON when commands are run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
