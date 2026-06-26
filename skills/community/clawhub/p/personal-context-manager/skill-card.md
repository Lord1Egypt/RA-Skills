## Description: <br>
Personal Context Manager helps users record daily reflections, integrate external information, refine a minimal personal knowledge core, generate cognitive maps, and request optional idea-sprouting or diary-feedback prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lj22503](https://clawhub.ai/user/lj22503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to maintain a local personal knowledge base: journal meaningful events, attach personal judgments to imported content, build connections, and periodically refine a concise core context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores personal reflections and imported content in local files, which can expose sensitive or third-party information if users save it indiscriminately. <br>
Mitigation: Avoid recording secrets or private work material without permission, and review stored notes before sharing or syncing the workspace. <br>
Risk: The entropy cleanup workflow can delete notes when run with force deletion. <br>
Mitigation: Run cleanup in dry-run mode first, review the generated deletion report, and back up notes before using --force. <br>
Risk: External content may be sorted or reused with incomplete source quality signals. <br>
Mitigation: Use the skill's source-level labels as triage cues and verify important external claims before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lj22503/personal-context-manager) <br>
- [Publisher profile](https://clawhub.ai/user/lj22503) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notes, structured Markdown files, concise guidance, shell commands, and local configuration or script updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local personal context files under journal, external, core, and connections directories; the entropy cleanup script supports dry-run and force deletion modes.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
