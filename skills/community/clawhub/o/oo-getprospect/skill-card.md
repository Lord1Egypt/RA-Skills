## Description: <br>
GetProspect (getprospect.com). Use this skill for ANY GetProspect request - searching and reading data. Whenever a task involves GetProspect, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate GetProspect through an OOMOL-connected account for business email discovery, email verification, contact lookup, and structured company or lead searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate against a real OOMOL-connected GetProspect account when explicitly used. <br>
Mitigation: Inspect the live connector schema before constructing payloads, run read actions directly, and confirm exact payloads and effects before any write or destructive action. <br>
Risk: Setup, connection, credential, or billing failures can block execution or send the user into account-management flows. <br>
Mitigation: Run first-time setup, reconnection, or billing-related steps only after a command fails with the matching error. <br>


## Reference(s): <br>
- [GetProspect homepage](https://getprospect.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-getprospect) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution and returns connector responses as JSON when commands are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
