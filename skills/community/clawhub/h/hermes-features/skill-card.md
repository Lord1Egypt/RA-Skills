## Description: <br>
Hermes-style self-improvement and memory management for OpenClaw agents, including a learning loop, skill system, and persistent memory with overflow archive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[protechsysipem-lang](https://clawhub.ai/user/protechsysipem-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add Hermes-style recurring self-review, skill proposal, and bounded persistent memory workflows to OpenClaw agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reviews prior sessions and writes persistent memory/profile files, which can retain sensitive or unnecessary user data. <br>
Mitigation: Exclude sensitive sessions and secrets, require explicit approval for memory writes, and define retention and deletion rules before use. <br>
Risk: Skill-changing behavior can introduce inaccurate or unsafe workflows into an agent's available skills. <br>
Mitigation: Require human approval before applying generated or updated skills, scan proposed changes, and keep rollback history. <br>
Risk: Cron and heartbeat automation can run recurring reviews without clear user intent. <br>
Mitigation: Make scheduled jobs auditable and disableable, and document when automated reviews run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/protechsysipem-lang/hermes-features) <br>
- [Publisher profile](https://clawhub.ai/user/protechsysipem-lang) <br>
- [Artifact README](artifact/README.md) <br>
- [Aquila Hermes features reference](artifact/aquila-hermes-features.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown instructions and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers session review, memory/profile file writes, overflow archives, and skill proposal workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
