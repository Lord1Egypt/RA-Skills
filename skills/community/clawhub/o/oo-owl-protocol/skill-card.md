## Description: <br>
Operates Owl Protocol through an OOMOL-connected account to read project information, retrieve token metadata, and patch token metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Owl Protocol data through the OOMOL oo CLI, including reading project summaries, retrieving token metadata, and preparing confirmed metadata updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to an OOMOL-connected Owl Protocol account. <br>
Mitigation: Install and use it only when the agent is intended to operate that connected Owl Protocol account. <br>
Risk: The patch_project_token action changes token metadata. <br>
Mitigation: Review the exact payload and intended effect with the user before running write actions. <br>
Risk: The optional first-time setup can run an external CLI installer. <br>
Mitigation: Avoid the installer unless the oo CLI is needed and the OOMOL installer is trusted in the execution environment. <br>


## Reference(s): <br>
- [ClawHub Owl Protocol Skill](https://clawhub.ai/oomol/oo-owl-protocol) <br>
- [Owl Protocol Homepage](https://owlprotocol.xyz) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use the OOMOL oo CLI and return JSON responses from Owl Protocol connector actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
