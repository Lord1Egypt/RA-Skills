## Description: <br>
Mailgun (mailgun.com). Use this skill for Mailgun requests that read, create, update, or delete data through the OOMOL Mailgun connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and support teams use this skill to manage Mailgun domains, templates, suppressions, tracking settings, and message sending through an OOMOL-connected account. It supports both read-only inspection and user-confirmed write or destructive Mailgun operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Mailgun account and may use sensitive credentials through the OOMOL connector. <br>
Mitigation: Use the OOMOL-connected account flow and avoid exposing raw Mailgun API tokens in prompts, files, or command arguments. <br>
Risk: Write actions can change Mailgun state, including sending email, changing tracking settings, creating templates, or adding suppression records. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running any action marked write. <br>
Risk: The delete_suppression action removes suppression or allowlist records. <br>
Mitigation: Get explicit approval for the target record before running destructive actions. <br>


## Reference(s): <br>
- [Mailgun homepage](https://www.mailgun.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-mailgun) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute Mailgun connector actions that return JSON data and an execution identifier.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
