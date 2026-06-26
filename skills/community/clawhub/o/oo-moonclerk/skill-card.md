## Description: <br>
MoonClerk (moonclerk.com). Use this skill for MoonClerk requests involving searching and reading customer, payment form, and payment data through the OOMOL-connected oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve and list MoonClerk customers, payment forms, and payments through an OOMOL-connected account. It is intended for read-oriented MoonClerk workflows where the agent should inspect the live action schema before invoking connector commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected MoonClerk account and can use stored service credentials through the oo CLI. <br>
Mitigation: Use it only in an authorized maintainer or developer context, and rely on OOMOL connection controls rather than exposing raw MoonClerk credentials to the agent. <br>
Risk: Connector inputs may vary by action or service version. <br>
Mitigation: Inspect the live action schema with `oo connector schema` before constructing each payload. <br>
Risk: Authentication, connection scope, credential expiry, app readiness, or billing failures can stop connector execution. <br>
Mitigation: Run setup, reconnection, or billing steps only after the matching command failure is observed. <br>


## Reference(s): <br>
- [MoonClerk homepage](https://moonclerk.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-moonclerk) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are returned as JSON when commands are run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
