## Description: <br>
Manage, optimize, and troubleshoot OpenClaw memory through MEMORY.md curation, daily logs, memory search tuning, compaction survival, and vector or hybrid search configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WeAreAllSatoshiN](https://clawhub.ai/user/WeAreAllSatoshiN) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to set up, maintain, and troubleshoot durable agent memory, including daily logs, curated long-term memory, retrieval behavior, and compaction flushes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead agents to store conversation-derived memory automatically, including sensitive or unwanted information. <br>
Mitigation: Review where memory is written, keep memory files inspectable and deletable, and require explicit approval for durable memory writes when handling sensitive data. <br>
Risk: External embedding providers or memory plugins may process memory contents outside the local workspace. <br>
Mitigation: Use only approved providers, configure separate API keys deliberately, and exclude secrets or sensitive personal data from memory files before indexing. <br>


## Reference(s): <br>
- [OpenClaw Memory on ClawHub](https://clawhub.ai/WeAreAllSatoshiN/openclaw-mem) <br>
- [QMD backend](https://github.com/tobi/qmd) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing setup, troubleshooting, and maintenance recommendations for OpenClaw memory files and search configuration.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
