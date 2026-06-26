## Description: <br>
Guides developers through versioning and migration strategies for financially active AI agent commerce systems, including blue-green deployments, canary releases, rollback layers, and state migration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operations teams use this guide to plan safer migrations for commerce agents that hold wallet balances, reputation, escrow obligations, marketplace listings, and API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide includes live GreenHelix migration examples that can change budgets, escrows, keys, services, migrations, rollbacks, or other financial agent state. <br>
Mitigation: Start with the sandbox endpoint and require explicit human approval before running examples against any live agent or account. <br>
Risk: The skill references a GreenHelix API key that may grant read/write access to purchased API tools. <br>
Mitigation: Use a least-privilege key, keep it out of shared prompts and logs, and rotate it after testing or suspected exposure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/greenhelix-agent-migration-versioning) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API endpoint](https://api.greenhelix.net/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guide with Python examples and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-executable guide; examples reference GREENHELIX_API_KEY for authenticated GreenHelix operations.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
