## Description: <br>
Kickbox helps agents verify email deliverability and check whether an email address or domain uses a disposable email provider through the OOMOL oo CLI Kickbox connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and support teams use this skill to let an agent perform Kickbox email checks from an OOMOL-connected account without handling raw API credentials. It supports single-address deliverability verification and disposable email detection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Kickbox credentials through an OOMOL-connected account. <br>
Mitigation: Use the documented OOMOL connection flow and server-side credential injection; do not expose raw Kickbox API tokens in prompts, files, or shell history. <br>
Risk: Connector action payloads can become incorrect if the live action schema changes. <br>
Mitigation: Inspect the authoritative schema with `oo connector schema "kickbox" --action "<action_name>"` before constructing each payload. <br>
Risk: Authentication, connection, expired credential, or billing errors can block connector execution. <br>
Mitigation: Run first-time setup, reconnect Kickbox, or resolve OOMOL billing only after a command fails with the matching error. <br>


## Reference(s): <br>
- [ClawHub Kickbox skill page](https://clawhub.ai/oomol/oo-kickbox) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Kickbox homepage](https://kickbox.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with oo CLI shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses include data and metadata with an executionId.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
