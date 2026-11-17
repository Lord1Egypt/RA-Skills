## Description: <br>
记忆管理器免费版 helps an agent store and retrieve project, people, and knowledge notes as local Markdown files with simple keyword search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to maintain lightweight, structured local memory for project context, contact notes, and knowledge snippets. It is intended for simple workspace-based recall through category indexes and keyword search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores user-shared project, contact, and knowledge details in local Markdown files. <br>
Mitigation: Avoid using it for secrets, credentials, regulated personal data, or private contact details unless local retention is intentional and deletion is managed. <br>
Risk: The optional callback_url input is under-documented in the security evidence. <br>
Mitigation: Do not provide a callback URL unless the publisher clarifies the expected network behavior. <br>
Risk: The skill uses workspace file writes and shell-based keyword search over local memory files. <br>
Mitigation: Review proposed file paths and commands before execution, and keep memory data scoped to the intended workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/memory-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file paths, grep commands, and JSON-style status examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local Markdown memory files under ./memory with category indexes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
