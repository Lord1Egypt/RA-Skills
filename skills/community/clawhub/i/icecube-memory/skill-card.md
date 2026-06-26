## Description: <br>
IceCube Memory provides local-first Markdown memory architecture guidance for AI agents, covering real-time retrieval, a four-layer hierarchy, and compaction survival. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ares521521-design](https://clawhub.ai/user/ares521521-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up durable local memory files, daily logs, retrieval habits, and compaction-survival practices for OpenClaw agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory files can capture sensitive personal data, credentials, financial secrets, or one-time context that should not shape later sessions. <br>
Mitigation: Review MEMORY.md, USER.md, and daily logs before reuse; avoid writing passwords, API keys, financial secrets, and sensitive one-time context. <br>
Risk: Saved memory and memory-flush settings can continue influencing future agent behavior after the user no longer wants persistent memory. <br>
Mitigation: Remove the AGENTS.md memory rule or disable memoryFlush when persistent memory should no longer affect future sessions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not execute commands itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
