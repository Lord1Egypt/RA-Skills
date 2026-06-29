## Description: <br>
MOCO (mocoapp.com). Use this skill for MOCO searching and read-only data retrieval through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to retrieve MOCO profile, company, and contact information through the OOMOL CLI without handling raw MOCO API tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First-time setup may require installing the third-party oo CLI. <br>
Mitigation: Review the oo CLI installer before running first-time setup, as recommended by the security guidance. <br>
Risk: A future version could add write or destructive MOCO actions. <br>
Mitigation: Require explicit user approval before executing any action tagged write or destructive. <br>


## Reference(s): <br>
- [MOCO homepage](https://www.mocoapp.com) <br>
- [OOMOL oo CLI repository](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-moco) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution; current documented actions are read-only get and list operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
