## Description: <br>
Self-evolving AI Agent with thinking chain, knowledge graph, emotion system, and Claude Code-inspired execution flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenqin1688](https://clawhub.ai/user/wenqin1688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to give an assistant a persistent thinking, memory, reflection, learning, and execution workflow for iterative task handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an autonomous agent command execution, file-writing, self-modification, and sub-agent capabilities without enough containment or user-control rules. <br>
Mitigation: Install only after reviewing the scripts and use it in a sandboxed OpenClaw workspace. <br>
Risk: Full command execution could allow untrusted or unintended commands to affect local files or processes. <br>
Mitigation: Keep permission_level limited or disabled, review every command before it runs, and do not store secrets or sensitive files where the agent can read or modify them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wenqin1688/her-agent) <br>
- [Publisher profile](https://clawhub.ai/user/wenqin1688) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and text responses with optional shell commands, code snippets, and JSON-backed memory records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an eight-turn execution flow, token budget controls, persistent memory files, and limited command permissions by default.] <br>

## Skill Version(s): <br>
3.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
