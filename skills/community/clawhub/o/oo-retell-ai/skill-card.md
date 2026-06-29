## Description: <br>
This skill lets an agent retrieve and list Retell AI calls, phone numbers, voices, and voice agents through the OOMOL retell_ai connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and support teams use this skill to inspect Retell AI account data through an OOMOL-connected account. It supports read-only lookup and listing workflows for calls, phone numbers, voices, and voice agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a connected Retell AI account through OOMOL, which gives the agent read access to Retell AI calls, phone numbers, voices, and voice agents on request. <br>
Mitigation: Install and use the skill only for workspaces where that read access is acceptable, and keep Retell AI scopes aligned with the intended use. <br>
Risk: First-time setup can involve installing the oo CLI from a remote installer. <br>
Mitigation: Use the installer only when the oo CLI is needed and OOMOL is trusted for the environment. <br>
Risk: Connector payloads that do not match the live action schema may produce failed or unintended requests. <br>
Mitigation: Inspect the live connector schema with oo connector schema before running an action, then send a JSON payload that matches the returned contract. <br>


## Reference(s): <br>
- [ClawHub Retell AI skill page](https://clawhub.ai/oomol/oo-retell-ai) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Retell AI homepage](https://www.retellai.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return JSON data from the OOMOL connector when executed with a connected Retell AI account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
