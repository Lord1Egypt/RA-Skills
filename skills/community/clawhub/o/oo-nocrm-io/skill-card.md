## Description: <br>
noCRM.io connector for agents to read, create, update, and delete noCRM.io data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate a connected noCRM.io CRM account from an agent, including lead creation, assignment, tagging, status changes, duplication, deletion, and team listing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can change or delete CRM lead records through the connected noCRM.io account. <br>
Mitigation: Require explicit user confirmation for every state-changing action, including appending descriptions, changing status, tagging, assigning, duplicating, creating, and deleting leads. <br>
Risk: Some state-changing actions are not tagged as write actions in the skill text. <br>
Mitigation: Treat action behavior and the live connector schema as authoritative, and confirm the exact target, payload, and intended effect before running any action that can modify CRM data. <br>
Risk: First-time setup may run remote CLI installation or account-connection commands. <br>
Mitigation: Run setup only after an auth or connection failure and only when the user trusts OOMOL and intends to connect the noCRM.io account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-nocrm-io) <br>
- [noCRM.io homepage](https://www.nocrm.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [noCRM.io icon](https://static.oomol.com/logo/third-party/NoCRM.io.svg) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution and returns connector JSON responses when actions are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
