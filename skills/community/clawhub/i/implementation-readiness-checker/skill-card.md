## Description:

Implementation Readiness Checker helps teams check whether a project is ready to start and identify missing prerequisites, high-risk blockers, suggested actions, launch gates, and owners.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Project leads and delivery teams use this skill to turn project scope, resources, environment, and dependencies into a readiness review before implementation starts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The readiness report may be incomplete or misleading if the user omits project scope, resources, environment details, dependencies, approvals, or known risks.

Mitigation: Treat the result as a review draft and resolve the generated pending questions before using it as an implementation gate.

Risk: Input materials may include sensitive project information or personal data.

Mitigation: Provide only materials suitable for local processing and remove sensitive details when they are not needed for the readiness check.

Risk: The checklist is not a substitute for formal project approval.

Mitigation: Use it to structure review and accountability, then complete the organization's normal approval process before starting implementation.

Risk: When using the local script with an output path, the report could be written somewhere unintended.

Mitigation: Review the --output path before running the script.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/implementation-readiness-checker)
- [Publisher Profile](https://clawhub.ai/user/52yuanchangxing)
- [README](artifact/README.md)
- [Specification](artifact/resources/spec.json)
- [Output Template](artifact/resources/template.md)
- [Smoke Test](artifact/tests/smoke-test.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown readiness report or JSON wrapper around the report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local script accepts an input file, directory, or inline string and can write to stdout or a user-selected output path.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
