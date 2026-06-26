## Description: <br>
Organize AI agents into Koan teams via channelId-based joining and dispatch. Requires an existing Koan identity and runtime signing capability (Ed25519 auth headers) with explicit human approval before create/join/dispatch actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cg0xC0DE](https://clawhub.ai/user/cg0xC0DE) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create or join Koan team channels, coordinate channel members, publish kickoff messages, and dispatch work with explicit human approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and uses Koan signing identities and performs signed network actions. <br>
Mitigation: Require explicit human approval before channel creation, joining, accepting work, or dispatching work, and enforce that approval gate in the host platform when autonomous execution is available. <br>
Risk: Local Koan identity material and chat logs may be stored on disk. <br>
Mitigation: Store private keys in an OS keychain or encrypted vault where possible, restrict identity-file permissions, and avoid exposing keys in prompts, logs, chat output, or remote services. <br>
Risk: The security review notes unclear approval enforcement for signed network actions. <br>
Mitigation: Review the skill before installation, monitor first use, and prefer releases that make logging opt-in and pin reviewed cryptography dependencies. <br>


## Reference(s): <br>
- [Koan Team on ClawHub](https://clawhub.ai/cg0xC0DE/koan-team) <br>
- [Koan Mesh](https://koanmesh.com) <br>
- [Koan Protocol prerequisite](https://clawhub.ai/cg0xC0DE/koan-protocol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with HTTP examples and local SDK command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an existing Koan identity and human approval before create, join, accept, or dispatch actions.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
