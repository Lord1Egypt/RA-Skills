## Description: <br>
SDD + Multica multi-agent development workflow for writing SDD specifications, creating and assigning Multica issues, planning dependency batches, monitoring progress, and recording completion updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[denghuayuan](https://clawhub.ai/user/denghuayuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to run feature work through an SDD-first, TDD-oriented Multica workflow, from specification documents through issue creation, dependency planning, progress checks, and closeout documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases may route ordinary feature-planning requests into the Multica SDD workflow. <br>
Mitigation: Narrow the trigger wording or require explicit user confirmation before invoking the workflow for a new task. <br>
Risk: The workflow includes state-changing actions such as creating or assigning Multica issues, editing specs, CLAUDE.md, and .multica/squad.md, and making git commits. <br>
Mitigation: Review the affected files and commands before execution, and require confirmation before running Multica issue operations or git commits. <br>
Risk: Some operational constraints are documented as project-specific and may not fit other repositories. <br>
Mitigation: Replace the example constraints with the target repository's own AGENTS.md, constitution, test, and typecheck requirements before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/denghuayuan/multica-sdd-workflow) <br>
- [Issue Templates](artifact/issue-templates.md) <br>
- [SDD Document Templates](artifact/sdd-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command snippets and reusable templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces SDD document structure, Multica issue descriptions, assignment commands, progress-check commands, and documentation update guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
