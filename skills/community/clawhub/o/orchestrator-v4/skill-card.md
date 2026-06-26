## Description: <br>
Intelligent task orchestration system that scans project scope, plans subtasks, dispatches multiple AI workers in parallel, supports module-based splitting for large projects, adaptive timeouts, rolling dispatch, and user-directed interruption or redirection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eviost](https://clawhub.ai/user/eviost) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to plan, split, and coordinate complex analysis, code generation, debugging, research, and batch-fix tasks across multiple AI workers. It is intended for codebase-scale work where module-aware task planning, concurrency limits, progress reporting, and resumable user control are useful. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically scan projects, spawn same-permission workers, and coordinate batch fixes across a codebase. <br>
Mitigation: Use it only in version-controlled workspaces, review the generated plan before dispatch, and inspect diffs after each batch. <br>
Risk: Fix mode can dispatch changes without strong built-in confirmation or rollback controls. <br>
Mitigation: Require manual approval before fix-mode dispatch and keep rollback available through source control. <br>
Risk: Project scans, plans, checkpoints, and logs can retain task context from sensitive workspaces. <br>
Mitigation: Avoid secrets-heavy directories and disable or clear checkpoints and logs when persistent task context is not acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eviost/orchestrator-v4) <br>
- [Publisher profile](https://clawhub.ai/user/eviost) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown progress reports, JSON task plans, shell commands, and generated or modified workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Plans include subtask descriptions, module keys, file-read caps, timeout estimates, and concurrency controls.] <br>

## Skill Version(s): <br>
2.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
