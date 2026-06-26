## Description: <br>
Inner Life Reflect helps an agent notice repeated behavior patterns, run quality-gated self-reflection, and update local reflection notes when meaningful changes appear. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DKistenev](https://clawhub.ai/user/DKistenev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users install this skill when they want an agent to detect repeated mistakes, behavior shifts, or stale self-model patterns and keep quality-gated local reflection notes. It is intended for agents using the openclaw-inner-life memory files and the inner-life-core prerequisite. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local self-reflection notes may influence future agent behavior. <br>
Mitigation: Periodically review memory/SELF.md and memory/habits.json and remove inaccurate, stale, or unwanted entries. <br>
Risk: The skill depends on inner-life-core memory files being initialized before reflection begins. <br>
Mitigation: Verify memory/inner-state.json and memory/habits.json exist before use; if they are missing, install and initialize inner-life-core first. <br>
Risk: Low-quality or repetitive reflections could add misleading self-model entries. <br>
Mitigation: Apply the documented specificity, evidence, novelty, and usefulness checks, and skip SELF.md updates when any check fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DKistenev/inner-life-reflect) <br>
- [Publisher profile](https://clawhub.ai/user/DKistenev) <br>
- [Skill-declared homepage](https://github.com/DKistenev/openclaw-inner-life) <br>
- [Skill-declared source path](https://github.com/DKistenev/openclaw-inner-life/tree/main/skills/inner-life-reflect) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local reflection notes to memory/SELF.md and update memory/habits.json after quality gates pass.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
