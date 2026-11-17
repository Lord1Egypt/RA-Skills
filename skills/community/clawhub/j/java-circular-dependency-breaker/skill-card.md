## Description:

Breaks circular dependencies in Java multi-module Gradle and Maven projects using interface extraction and business service separation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naozixu](https://clawhub.ai/user/naozixu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and verify Java multi-module refactors that break Gradle or Maven dependency cycles while preserving Spring wiring and test behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to guide changes to Java source and build files, including dependency removal.

Mitigation: Review proposed source and build-file changes before applying them, and verify affected modules compile and tests pass.

Risk: Rollback and cleanup commands can discard local project changes if used carelessly.

Mitigation: Inspect the working tree and confirm the rollback target before running recovery commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/naozixu/skills/java-circular-dependency-breaker)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Java examples, build-file guidance, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces refactoring plans, checkpoints, verification commands, and rollback guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
