## Description:

Reviews Kotlin, Java, Swift and Dart code and diffs in Android, iOS and Flutter apps for correctness, concurrency, lifecycle leaks, UI performance, architecture, error handling, tests, accessibility and i18n. Reports Blocker, Major, Minor and Nit findings with file:line and fix snippets, then an Approve or Request changes verdict. Use when reviewing a pull request, merge request, diff, branch or file before merging mobile code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

Mobile developers use this skill to review Android, iOS and Flutter changes before merging. It checks code in the chosen review scope and returns prioritized findings with explanations, fix snippets, questions and a verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A scoped code review can miss issues or produce findings that need more context; it is not a full security audit.

Mitigation: Set the intended review scope, verify findings against the code and its stated intent, and use a dedicated security review when a full audit is needed.

## Reference(s):

- [Kotlin and Android review reference](artifact/references/kotlin.md)
- [Java and Android review reference](artifact/references/java.md)
- [Swift review reference](artifact/references/swift.md)
- [Dart and Flutter review reference](artifact/references/dart.md)
- [ClawHub skill release](https://clawhub.ai/ahmadhussain0335/skills/mobile-code-review)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code]

**Output Format:** [Markdown review with severity-ranked findings, file:line locations, fix snippets, questions, clean checks and a verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings use Blocker, Major, Minor or Nit severity; Blocker and Major findings include a minimal fix snippet.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter; server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
