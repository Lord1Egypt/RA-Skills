## Description: <br>
Personal AI (personal.ai) lets agents read, create, and update data through an OOMOL-connected Personal AI account instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent operate Personal AI personas, send messages or instructions, and upload memories, text documents, or public URLs through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and write Personal AI data through a connected account, including content that may persist in memories or document libraries. <br>
Mitigation: Install it only for intended Personal AI account use, and review proposed write payloads before approving state-changing actions. <br>
Risk: Incorrect payloads could send unintended persona messages, instructions, memories, documents, or URL uploads. <br>
Mitigation: Inspect the live connector schema before constructing payloads and confirm the exact effect with the user for write actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-personal-ai) <br>
- [Personal AI homepage](https://personal.ai) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector actions may return JSON responses containing data and meta.executionId; write actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
