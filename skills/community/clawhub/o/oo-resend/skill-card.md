## Description: <br>
Enables an agent to operate Resend through an OOMOL-connected account using the oo CLI instead of calling the Resend API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send email through Resend from an OOMOL-connected account after inspecting the live connector schema and confirming write payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send email through Resend, which can contact external recipients or send incorrect content if the payload is wrong. <br>
Mitigation: Approve the exact recipient, content, and payload before running the write action. <br>
Risk: The skill depends on an OOMOL-connected Resend account and sensitive credential handling. <br>
Mitigation: Confirm the user is comfortable connecting Resend through OOMOL and rely on OOMOL server-side credential injection rather than exposing raw tokens. <br>
Risk: First-time setup commands install or authenticate the oo CLI and should not be run automatically during normal use. <br>
Mitigation: Treat install, login, connection, and billing commands as one-time setup steps used only after matching command failures. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-resend) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>
- [Resend Homepage](https://resend.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live connector schema inspection before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
