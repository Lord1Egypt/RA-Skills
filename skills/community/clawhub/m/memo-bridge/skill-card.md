## Description: <br>
MemoBridge helps agents export, import, back up, migrate, and transfer AI memory or context between supported AI tools, including CodeBuddy, OpenClaw, Hermes Agent, Claude Code, Cursor, ChatGPT, Doubao, and Kimi. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gonelake](https://clawhub.ai/user/gonelake) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI assistant users use this skill to move persistent memory, preferences, project context, and assistant history between supported local and prompt-guided AI tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to use a local MemoBridge CLI that can read, export, and rewrite persistent AI memory files. <br>
Mitigation: Install only a trusted and reviewed MemoBridge CLI, use explicit workspace paths, run dry-run first, inspect and redact memo-bridge.md before import or sharing, and back up existing memory files before write or overwrite operations. <br>


## Reference(s): <br>
- [ClawHub memo-bridge release page](https://clawhub.ai/gonelake/memo-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or instruct creation of memo-bridge.md interchange files and paste-ready prompts for cloud AI tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
