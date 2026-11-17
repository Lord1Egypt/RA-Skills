## Description: <br>
笔记工具包基础版 helps an agent capture, organize, search, and link personal notes through natural-language requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to direct an agent to manage personal notes, including quick capture, topic organization, retrieval, note linking, and meeting preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security verdict is suspicious because privacy and execution boundaries are unclear. <br>
Mitigation: Install only after reviewing the publisher's security guidance and confirming what note content or metadata can leave the local environment. <br>
Risk: The artifact requests local read, search, and command execution capabilities for note workflows. <br>
Mitigation: Run the skill in a workspace with limited file access and require confirmation before executing commands that read, write, search, or export notes. <br>
Risk: The artifact includes callback URL, API key, external API, and network behavior while also making local-only privacy claims. <br>
Mitigation: Disable or closely review callback and network features unless the publisher clarifies when external calls happen and what data is transmitted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/note-toolkit-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell command examples and JSON response structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The free edition describes single-task operation, optional configuration, local note files, and structured success/error responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
