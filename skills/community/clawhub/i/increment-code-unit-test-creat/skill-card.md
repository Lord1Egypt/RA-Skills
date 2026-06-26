## Description: <br>
Use when generating JUnit 5 + Mockito unit tests for Java/Maven source code, especially for incremental changes on a git branch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[endcy](https://clawhub.ai/user/endcy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create or update JUnit 5 and Mockito tests for Java/Maven code, including diff-based coverage for changes on a feature branch. It can also help identify missing Maven test dependencies and propose dependency or plugin configuration updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated tests or proposed dependency edits may be incorrect for the target repository's business logic or build constraints. <br>
Mitigation: Review generated tests and pom.xml edits before committing, then run Maven test compilation and targeted tests on a feature branch. <br>
Risk: Running Maven commands in an untrusted repository can execute project-controlled build logic. <br>
Mitigation: Use the skill only in repositories you trust or in an isolated environment, and avoid running Maven builds until repository contents are reviewed. <br>
Risk: Diff-based generation depends on the selected default branch and may miss relevant behavior outside the changed files. <br>
Mitigation: Confirm the comparison branch, inspect dependent classes, and supplement with full-class tests when incremental coverage is insufficient. <br>


## Reference(s): <br>
- [Skill README](artifact/README.md) <br>
- [Maven Dependency Configuration Reference](artifact/references/dependency-config.md) <br>
- [JUnit 5 and Mockito Test Template Reference](artifact/references/test-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/endcy/increment-code-unit-test-creat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Java, XML, and shell command snippets; may include proposed file edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates or updates JUnit 5 and Mockito tests, may propose Maven pom.xml dependency changes after confirmation, and may run Maven test commands for validation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
