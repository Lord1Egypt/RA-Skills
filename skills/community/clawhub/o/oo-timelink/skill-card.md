## Description: <br>
This skill helps agents search and read Timelink data through an OOMOL-connected account using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs read-only access to Timelink clients, projects, services, users, time entries, company details, or token metadata through an existing OOMOL connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read Timelink business data available through the connected OOMOL account. <br>
Mitigation: Install and use it only when the user trusts OOMOL's oo CLI and is comfortable granting the agent read access through that connected account. <br>
Risk: Action schemas may change or differ from assumptions in a prompt. <br>
Mitigation: Inspect the live action schema with the oo CLI before constructing command payloads. <br>
Risk: Setup commands can alter local CLI authentication or connection state. <br>
Mitigation: Run authentication, connection, installer, or billing-recovery steps only after an actual setup-related failure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-timelink) <br>
- [Timelink homepage](https://timelink.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include oo CLI commands, action names, JSON payloads, and setup guidance for authentication, connection, or billing errors.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
