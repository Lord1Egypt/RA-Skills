## Description: <br>
Superchat connector for reading, creating, updating, and messaging Superchat data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Superchat workspace data, manage contacts, and send Superchat email, text, or WhatsApp template messages through the OOMOL oo CLI connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Superchat account and uses OOMOL server-side credential handling. <br>
Mitigation: Install only if you trust OOMOL and are comfortable connecting the Superchat account through the OOMOL CLI. <br>
Risk: Write actions can create or update contacts and send outbound email, text, or WhatsApp template messages. <br>
Mitigation: Confirm the exact payload and intended effect with the user before running write actions. <br>
Risk: The first-time setup guidance includes shell commands that install the oo CLI from remote URLs. <br>
Mitigation: Prefer a verified package or documented installer path, and review install commands before execution. <br>


## Reference(s): <br>
- [ClawHub Superchat skill](https://clawhub.ai/oomol/oo-superchat) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Superchat homepage](https://www.superchat.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with oo CLI shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before action payloads; write actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
