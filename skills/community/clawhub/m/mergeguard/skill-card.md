## Description:

MergeGuard reviews AI-generated code before merge and produces strict merge/no-merge recommendations covering correctness, scope, security and privacy, dependency and configuration risk, missing tests, validation evidence, and required fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brasco05](https://clawhub.ai/user/brasco05)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use MergeGuard to review PRs, diffs, branches, patches, local changes, or agent-written code before merge. It helps identify correctness, security, privacy, scope, dependency, configuration, and validation issues that should block or shape a merge decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect repositories and encourage running tests or build checks, which can be risky in untrusted codebases.

Mitigation: Review commands before execution and run only the smallest meaningful validation gate for the change.

Risk: A merge recommendation can be unreliable when important PR, diff, CI, or repository context is unavailable.

Mitigation: Limit the review to visible evidence and use BLOCKED or require fixes when missing context prevents a safe decision.

## Reference(s):

- [MergeGuard ClawHub skill page](https://clawhub.ai/brasco05/skills/mergeguard)
- [Source skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown review report with decision, risk, confidence, findings, validation status, and required fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes one merge decision: MERGE, FIX FIRST, REJECT, or BLOCKED.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
