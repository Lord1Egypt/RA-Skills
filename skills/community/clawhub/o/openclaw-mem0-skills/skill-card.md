## Description: <br>
Persistent long-term memory across sessions that helps an agent remember a user's identity, preferences, rules, technical stack, and projects using Mem0. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kartik-mem0](https://clawhub.ai/user/kartik-mem0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to build, review, export, and hand off persistent user memory across sessions. It supports onboarding, memory maintenance, markdown export, and concise briefings for new agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored long-term memory can contain sensitive personal or work context. <br>
Mitigation: Do not store secrets, credentials, regulated data, private customer information, or highly confidential employer details; use review and delete workflows regularly. <br>
Risk: The skill cannot operate unless the Mem0 plugin and API key are configured. <br>
Mitigation: Run the prerequisite setup and confirm MEM0_API_KEY is configured before using memory workflows. <br>


## Reference(s): <br>
- [Mem0](https://mem0.ai) <br>
- [Mem0 API Keys](https://app.mem0.ai/dashboard/api-keys) <br>
- [ClawHub Skill Page](https://clawhub.ai/kartik-mem0/openclaw-mem0-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the openclaw-mem0 plugin and MEM0_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
