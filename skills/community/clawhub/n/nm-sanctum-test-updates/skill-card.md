## Description: <br>
Updates, generates, and validates tests using git-workspace context and TDD/BDD methodology. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to maintain test coverage after code changes, generate TDD/BDD test scaffolding, improve existing tests, and validate test quality before commit or CI review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated tests or TDD-driven code changes may encode incorrect assumptions about the codebase. <br>
Mitigation: Use explicit targets, review generated tests and any related code changes before committing, and run the relevant test suite to verify behavior. <br>
Risk: Broad testing requests may activate the skill across large repositories and produce noisy or costly recommendations. <br>
Mitigation: Start with a focused path or module for large repositories, then expand only after reviewing the first results. <br>
Risk: Invariant-encoding tests can force architecture decisions when an invariant changes. <br>
Mitigation: Treat changes to invariant tests as human review points and decide whether to preserve, layer around, or revise the invariant. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/skills/nm-sanctum-test-updates) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/athola) <br>
- [OpenClaw Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose test scaffolding, pytest commands, coverage checks, and review checklists for user-selected targets.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
