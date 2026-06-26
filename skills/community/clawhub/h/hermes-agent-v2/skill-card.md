## Description: <br>
NousResearch Hermes Agent CLI integration for running Hermes commands, using context files, delegating sub-agent tasks, searching or adding memory notes, managing Hermes skills, and checking status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wihy](https://clawhub.ai/user/wihy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to invoke the Hermes CLI from an agent workflow for question answering, contextual runs, delegation, memory operations, skill management, and health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer a high-capability agent runtime through the Hermes CLI, including delegation, browser automation, code execution, and persistent memory features when enabled in Hermes. <br>
Mitigation: Install it only for intended Hermes administration, review Hermes configuration changes before applying them, and enable delegation, browser automation, public endpoints, or persistent memory only when those capabilities are required. <br>
Risk: Hermes provider keys may be exposed if copied into chat, committed to source control, or stored with overly broad local file permissions. <br>
Mitigation: Keep provider keys out of chat and repositories, store them only in the local Hermes environment file, and restrict permissions on that file. <br>


## Reference(s): <br>
- [Hermes Agent GitHub repository](https://github.com/NousResearch/hermes-agent) <br>
- [ClawHub skill page](https://clawhub.ai/wihy/hermes-agent-v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill produces Hermes CLI invocations and operator guidance; command effects depend on the local Hermes installation and configuration.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
