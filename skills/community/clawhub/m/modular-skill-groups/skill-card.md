## Description: <br>
Organize and switch between named skill groups to keep agent context focused, list available groups, and manage skill assignments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[di5cip1e](https://clawhub.ai/user/di5cip1e) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to activate named skill groups, list available groups, and keep the context window focused during different project phases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The active skill group persists across sessions and may cause the agent to use an unexpected skill set. <br>
Mitigation: Review the predefined groups before activation and check ~/.openclaw/active_skill_group if the agent appears to be using an unexpected skill set. <br>


## Reference(s): <br>
- [Skill group definitions](references/SKILL_GROUPS.md) <br>
- [ClawHub release page](https://clawhub.ai/di5cip1e/modular-skill-groups) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist the selected group in ~/.openclaw/active_skill_group.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
