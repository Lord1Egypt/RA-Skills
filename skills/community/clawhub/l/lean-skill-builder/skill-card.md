## Description: <br>
Builds lean SKILL.md-based skills by helping agents decide when a skill is justified, draft a minimal skeleton, and audit existing skills for bloat and drift. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zurbrick](https://clawhub.ai/user/zurbrick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to decide whether reusable skill guidance is warranted, create minimal skill skeletons, and tighten existing skills without adding unnecessary process or files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trigger-writing advice may become too broad if copied without review. <br>
Mitigation: Review generated trigger descriptions for specificity and run near-miss smoke tests before publishing a skill. <br>
Risk: Generated skill edits or skeletons could introduce incorrect or misleading guidance. <br>
Mitigation: Audit generated skill content before deployment and keep supporting files limited to material that directly improves reliability. <br>


## Reference(s): <br>
- [Skill Builder on ClawHub](https://clawhub.ai/zurbrick/lean-skill-builder) <br>
- [Decision Tree](references/decision-tree.md) <br>
- [Supporting Files Guide](references/supporting-files-guide.md) <br>
- [Writing Patterns](references/writing-patterns.md) <br>
- [Frontmatter Patterns](references/frontmatter-patterns.md) <br>
- [Audit Checklist](references/audit-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional code blocks, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should stay concise and focused on the smallest justified skill change or build plan.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
