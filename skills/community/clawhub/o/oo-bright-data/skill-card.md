## Description: <br>
Bright Data helps an agent search and read Bright Data account, marketplace dataset, dataset view, snapshot metadata, and snapshot delivery information through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Bright Data read actions from an agent without handling raw Bright Data tokens directly. It is suited for checking account capability, listing marketplace datasets and views, and retrieving dataset or snapshot metadata through the connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an installed oo CLI, an authenticated OOMOL session, an active Bright Data connection, and available billing credit. <br>
Mitigation: Run setup or recovery steps only after the matching CLI, authentication, connection, scope, credential, app, or billing error appears, then retry the requested read action. <br>
Risk: Future connector actions tagged as write or destructive could change or remove Bright Data state if executed without checking the exact target and payload. <br>
Mitigation: Inspect the live connector schema, explain the intended target and payload, and get explicit user approval before running any tagged write or destructive action. <br>
Risk: Connector payloads can drift if the Bright Data action contract changes. <br>
Mitigation: Fetch the action schema with the oo CLI before constructing each payload and match the current input fields exactly. <br>


## Reference(s): <br>
- [Bright Data skill on ClawHub](https://clawhub.ai/oomol/skills/oo-bright-data) <br>
- [Bright Data homepage](https://brightdata.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before action payload construction.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
