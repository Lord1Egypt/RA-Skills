## Description: <br>
Bilingual EN/ZH project lifecycle navigator for non-technical users and AI Coding Agent workflows, routing users through new project intake, mid-project realignment, or code review and upgrade planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[englandtong](https://clawhub.ai/user/englandtong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, non-technical builders, founders, operators, PMs, and AI Coding Agent users use this skill to clarify new project requirements, recalibrate drifting projects, or turn an existing codebase review into an actionable upgrade plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may provide sensitive project files or code during review. <br>
Mitigation: Share only code the user is comfortable having the agent inspect; remove secrets before review, and rotate any exposed secrets found in code. <br>
Risk: Generated deletion, refactor, or upgrade recommendations could be applied without sufficient review. <br>
Mitigation: Treat recommendations as plans to verify, test, and approve before execution, with rollback steps for material changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/englandtong/project-lifecycle-navigator) <br>
- [README](README.md) <br>
- [Usage examples](examples/usage-examples.md) <br>
- [New project intake prompt](prompts/en/01-new-project-intake.en.md) <br>
- [Mid-project realignment prompt](prompts/en/02-midproject-realignment.en.md) <br>
- [Code review and upgrade prompt](prompts/en/03-code-review-upgrade.en.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Structured Markdown reports, question sets, plans, task queues, checklists, and occasional verification commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English/Chinese output follows the user's language by default; recommendations are intended for human or Coding Agent review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, skill.json, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
