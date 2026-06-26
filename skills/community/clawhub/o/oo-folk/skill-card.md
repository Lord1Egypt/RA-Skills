## Description: <br>
folk (folk.app). Use this skill for any folk request: reading, creating, updating, and deleting data through the OOMOL oo CLI connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent read, create, update, and delete folk CRM people, companies, groups, users, and related custom-field data through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify folk CRM data through an OOMOL-connected account. <br>
Mitigation: Install it only when the agent should operate folk data through OOMOL, and review create or update payloads before approval. <br>
Risk: Delete actions can remove folk people or companies. <br>
Mitigation: Require explicit user confirmation of the target record and intended effect before running destructive actions. <br>
Risk: The optional oo CLI installer runs a remote installation script. <br>
Mitigation: Run the installer only when the CLI is needed and the user trusts OOMOL's installer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-folk) <br>
- [folk homepage](https://folk.app) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include oo CLI connector commands, schema inspection guidance, JSON action payloads, and confirmation prompts for write or delete actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
