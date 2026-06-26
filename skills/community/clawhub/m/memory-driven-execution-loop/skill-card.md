## Description: <br>
Deterministic external-memory execution loop using rules/goal/plan/progress/notes/lessons with strict preflight, one-step execution, and measurable lesson quality gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kdylan1010-alt](https://clawhub.ai/user/kdylan1010-alt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run work from explicit Markdown memory files, enforce one clear next action, record reasoning and progress, and turn failures into reusable lessons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent task memory files can accumulate sensitive, stale, or unrelated project information if they are not curated. <br>
Mitigation: Keep rules.md, goal.md, plan.md, progress.md, notes.md, and lessons.md in a trusted project folder, review them before use, and avoid storing secrets or unrelated private information in those files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Files] <br>
**Output Format:** [Markdown guidance and file-update instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires trusted local rules.md, goal.md, plan.md, progress.md, notes.md, and lessons.md files; no executable code, installs, credentials, or network behavior.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
