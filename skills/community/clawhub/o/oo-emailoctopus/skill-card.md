## Description: <br>
EmailOctopus lets an agent operate EmailOctopus through the OOMOL oo CLI to read campaigns, lists, and contacts and to create, update, or delete contacts with confirmation for state-changing actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage EmailOctopus marketing data from an agent through their OOMOL-connected account. It supports campaign, list, and contact lookup plus contact creation, updates, and deletion when the user can review and approve state-changing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate an EmailOctopus account through OOMOL-managed credentials. <br>
Mitigation: Install only when the agent should access that account, and keep OOMOL and EmailOctopus account access limited to intended users. <br>
Risk: Contact creation, updates, and deletion can change or remove EmailOctopus data. <br>
Mitigation: Review the exact action payload and target, then require explicit user approval before running write or destructive actions. <br>
Risk: First-time setup may involve remote installer commands for the oo CLI. <br>
Mitigation: Prefer the official oo CLI install guide or verify installer contents before running remote install commands. <br>


## Reference(s): <br>
- [ClawHub EmailOctopus skill page](https://clawhub.ai/oomol/oo-emailoctopus) <br>
- [EmailOctopus homepage](https://emailoctopus.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with oo CLI shell commands and JSON payload examples; connector responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution and requires user confirmation for write or destructive actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
