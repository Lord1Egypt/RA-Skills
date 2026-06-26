## Description: <br>
Review an OpenClaw skill for token efficiency, scriptability, and clean action boundaries; back up first, then improve the skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kid0114](https://clawhub.ai/user/kid0114) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this meta-skill to review and improve OpenClaw skills for token efficiency, scriptability, and clearer action boundaries. It is intended for local skill-review workflows where backing up target files before modification is required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect and modify local skill folders, including SKILL.md, references, scripts, and other local skill files. <br>
Mitigation: Back up target skill files before making changes, review proposed edits, and show backup paths plus modification evidence after changes. <br>
Risk: Review output may be Chinese-language, which may not fit every workflow. <br>
Mitigation: Install only where Chinese-language review output is acceptable, or adjust the skill instructions before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kid0114/master-skill-review) <br>
- [Skill Review Checklist](references/checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown review output with optional shell commands and checklist-style guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review output may be in Chinese and may include suggested changes, backup paths, and evidence of modifications.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
