## Description:

A Chinese-language guidance skill that helps developers design, review, and write Java unit tests using consistent equivalence class, boundary value, decision table, state transition, assertion, and mocking practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baixuanzhu](https://clawhub.ai/user/baixuanzhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to decide what Java unit tests to write, how many cases are sufficient, and how to map those cases into JUnit and Mockito code while staying aligned with team testing standards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording around unit-testing questions may activate the skill during general testing discussions.

Mitigation: Confirm that Java unit-test guidance is relevant before applying recommendations.

Risk: Generated dependency, configuration, or test-code changes may not match the project's existing test stack or conventions.

Mitigation: Review proposed JUnit, Mockito, AssertJ, Spring Boot, and coverage-tool changes against the target project before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baixuanzhu/skills/java-unit-test)
- [01 - Test Design Foundations](references/01-test-design-foundations.md)
- [02 - Equivalence and Boundary](references/02-equivalence-and-boundary.md)
- [03 - Decision Table](references/03-decision-table.md)
- [04 - State Transition](references/04-state-transition.md)
- [05 - Coverage and Quantity](references/05-coverage-and-quantity.md)
- [06 - Tools Lean](references/06-tools-lean.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Java, JUnit, Mockito, dependency, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language guidance; no executable code, persistence, credential handling, or hidden data movement reported by security evidence]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
