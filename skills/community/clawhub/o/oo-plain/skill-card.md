## Description: <br>
Plain helps an agent read, create, and update Plain customer data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support operators, and other authorized users use this skill to look up Plain customers and create or update customer records after confirming write payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials through the OOMOL-connected Plain account. <br>
Mitigation: Install only when the user intends to operate Plain through OOMOL, keep credentials in the OOMOL connection flow, and do not expose raw tokens to the agent. <br>
Risk: First-time setup may involve pipe-to-shell or PowerShell installer commands for the oo CLI. <br>
Mitigation: Use verified OOMOL CLI documentation, review installer contents before execution, and require explicit user approval before running installer commands. <br>
Risk: The upsert customer action can create or update Plain customer records. <br>
Mitigation: Inspect the live action schema before constructing payloads and confirm the exact write payload and expected effect with the user before execution. <br>


## Reference(s): <br>
- [Plain homepage](https://www.plain.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-plain) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read actions can be run directly; write actions require user confirmation of the exact payload and effect.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
