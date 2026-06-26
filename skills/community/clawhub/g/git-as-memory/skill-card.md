## Description: <br>
Provides a Git-backed memory policy and CLI workflow for agents to remember durable preferences, project decisions, conventions, lessons learned, and audit Git-native memory with gam. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[femto](https://clawhub.ai/user/femto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add durable, auditable project memory to Git repositories and guide agents on when to search, write, update, delete, and audit memory with gam. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may persist secrets or noisy one-off data as memory. <br>
Mitigation: Follow the documented memory policy, avoid secrets and credentials, search before writing, and store only stable, reusable information. <br>
Risk: Global installation of the external npm or pip package may introduce dependency provenance risk. <br>
Mitigation: Review the external package provenance before global installation and use the skill only in repositories where Git-ref memory storage is appropriate. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May report memory keys after writes; otherwise provides concise operational guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
