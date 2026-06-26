## Description: <br>
Guides Hermes Agent sessions through warmup, planning, building, recapping, wrapup, context loading, handoff verification, and project scaffolding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adelvillar1](https://clawhub.ai/user/adelvillar1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep project sessions consistent from startup through handoff. It helps load project context, draft plans, track acceptance criteria, write session recaps, and verify wrapup state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad discovery steps can read more workspace context than needed. <br>
Mitigation: Keep searches scoped to the current workspace and the user's current task. <br>
Risk: The workflow references local credential files, direct database queries, API queries, and production operations. <br>
Mitigation: Require explicit approval in the current turn before reading local credential files or running production, database, or API access. <br>
Risk: Plan, recap, and project-memory updates can introduce incorrect handoff guidance if accepted without review. <br>
Mitigation: Review proposed documentation writes and verify plan status against source files before saving. <br>


## Reference(s): <br>
- [Project Scaffold Reference](references/project-scaffold.md) <br>
- [Stale Data Verification](references/stale-data-verification.md) <br>
- [Publisher homepage](https://github.com/adelvillar1) <br>
- [ClawHub skill page](https://clawhub.ai/adelvillar1/project-methodology) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and reusable plan and recap templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose documentation writes for plans, recaps, and project memory after user review.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
