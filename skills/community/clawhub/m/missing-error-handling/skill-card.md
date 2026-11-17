## Description:

Code handles only the happy path: external calls, I/O, and parsing have no failure handling and crash on unexpected input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvogt99](https://clawhub.ai/user/mvogt99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to identify missing error handling around network, disk, subprocess, parsing, and third-party API interactions and to guide targeted fixes for safer failure behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying the skill may cause an agent to modify application error-handling paths.

Mitigation: Review resulting diffs, run relevant tests, and confirm changed failure behavior before merging or deploying.

Risk: Error logging guidance could expose sensitive arguments or internal failure details if applied without redaction.

Mitigation: Redact secrets and personal data in logs, and keep internal diagnostic detail separate from user-facing error messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mvogt99/skills/missing-error-handling)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code]

**Output Format:** [Markdown guidance with code-review recommendations and potential code edits when applied by an agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets macOS, Linux, and Windows according to ClawHub metadata.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
