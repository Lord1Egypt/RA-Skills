## Description: <br>
Memory Hub helps agents share and synchronize a Git-backed memory repository containing USER.md, KNOWLEDGE.md, RULES.md, and TOOLS.md across multiple agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dr23334444](https://clawhub.ai/user/dr23334444) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to install and operate a shared memory workflow across multiple agents, including reading, writing, syncing, searching, and merging memory entries from a user-controlled Git repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shared memory may contain personal preferences, operational context, or other sensitive information in a long-lived Git repository. <br>
Mitigation: Use a private repository you control, avoid secrets and highly sensitive personal details, and review USER.md, RULES.md, and TOOLS.md periodically. <br>
Risk: Agent-written memory updates may commit or push incorrect or overly broad information. <br>
Mitigation: Ask the agent to show exact changes before committing or pushing important memories. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dr23334444/memory-hub) <br>
- [Upgrade Guide](references/upgrade-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or perform Git-backed memory file updates after user-controlled setup and review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
