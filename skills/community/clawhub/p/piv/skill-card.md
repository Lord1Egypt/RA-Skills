## Description:

PIV workflow orchestrator - Plan, Implement, Validate loop for systematic multi-phase software development. Use when building features phase-by-phase with PRPs, automated validation loops, or multi-agent orchestration. Supports PRD creation, PRP generation, codebase analysis, and iterative execution with validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smokealot420](https://clawhub.ai/user/smokealot420)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to plan and execute multi-phase software work through PRD creation, PRP generation, codebase analysis, implementation, validation, debugging, and workflow tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can edit projects, run commands, spawn sub-agents, and create commits without clear approval safeguards.

Mitigation: Use it only on trusted repositories and require manual review of generated PRPs, planned file changes, validation commands, and commit messages before allowing execution or commits.

Risk: Generated PRPs or validation plans may introduce incorrect guidance or unsafe changes into a target project.

Mitigation: Review generated planning artifacts and validation commands before execution, and scan the skill before deployment.

## Reference(s):

- [FTW repository](https://github.com/SmokeAlot420/ftw)
- [ClawHub skill page](https://clawhub.ai/smokealot420/skills/piv)
- [Codebase analysis reference](references/codebase-analysis.md)
- [PRD creation reference](references/create-prd.md)
- [PRP generation reference](references/generate-prp.md)
- [PRP execution reference](references/execute-prp.md)
- [PIV executor reference](references/piv-executor.md)
- [PIV validator reference](references/piv-validator.md)
- [PIV debugger reference](references/piv-debugger.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create PRDs, PRPs, workflow tracker entries, implementation changes, validation reports, and commits in the target repository.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
