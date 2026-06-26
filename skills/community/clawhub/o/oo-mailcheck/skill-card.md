## Description: <br>
Mailcheck (usercheck.com). Use this skill for ANY Mailcheck request - searching and reading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Mailcheck through an OOMOL-connected account, including account status checks, domain validation, and single-email deliverability verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Mailcheck account and can fail when authentication, connection scope, app readiness, or billing state is invalid. <br>
Mitigation: Run setup or reconnection steps only after the corresponding command failure, and resolve billing or connection errors before retrying. <br>
Risk: Connector payloads may become invalid if the live Mailcheck action contract changes. <br>
Mitigation: Fetch the live action schema with `oo connector schema` before constructing each payload. <br>
Risk: Future Mailcheck actions tagged as write or destructive could change or remove remote data. <br>
Mitigation: Confirm the exact payload and effect with the user before write actions, and require explicit approval before destructive actions. <br>


## Reference(s): <br>
- [Mailcheck homepage](https://www.usercheck.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Mailcheck ClawHub page](https://clawhub.ai/oomol/oo-mailcheck) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before execution and returns connector results as JSON when actions run.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
