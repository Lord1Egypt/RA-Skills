## Description: <br>
Unified TDD skill with three input modes - from spec, from task, or from description. Enforces test-first development using repository patterns, with proptest guidance and backpressure integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ImBeasting](https://clawhub.ai/user/ImBeasting) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to make an agent follow a test-first workflow for implementation tasks, acceptance-criteria specs, and ad-hoc feature descriptions. It guides the agent through writing failing tests, making minimal implementation changes, refactoring, and reporting test or coverage evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause an agent to run local test, coverage, lint, audit, and build-status commands in a repository. <br>
Mitigation: Review the command scope and environment before execution, and confirm that any configured build-status destination is acceptable before using the ralph emit step. <br>
Risk: The skill guides an agent to create or modify tests and implementation code. <br>
Mitigation: Review generated diffs before committing and verify that tests fail for the intended reason before accepting implementation changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ImBeasting/imbeasting-test-driven-development) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs agents to produce tests, minimal implementation changes, refactors, and completion evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
