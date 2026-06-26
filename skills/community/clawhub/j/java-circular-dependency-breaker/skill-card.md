## Description: <br>
Break circular dependencies in Java multi-module Gradle/Maven projects using interface extraction and business service separation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[naozixu](https://clawhub.ai/user/naozixu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose and break circular dependencies in Java Gradle or Maven multi-module projects. It guides interface extraction, business service extraction, co-migration choices, and verification steps for preserving behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Refactoring guidance can lead to incorrect source moves or dependency removals if applied without review. <br>
Mitigation: Review suggested file moves and build-file edits before applying them, then compile and test all affected modules. <br>
Risk: Circular-dependency refactors can leave a Java project in a non-compiling state during migration. <br>
Mitigation: Keep git rollback steps available and restore the prior dependency or source tree before retrying if verification fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/naozixu/java-circular-dependency-breaker) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Java, Gradle, Maven, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes decision points, verification checklists, and rollback guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
