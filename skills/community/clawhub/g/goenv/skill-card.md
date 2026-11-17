## Description:

Provides a small Go library that reads `ENV` and reports `dev` only when its value is exactly `dev`, treating every other value as `prod`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use goenv in Go applications to branch between development and production behavior with `Get()`, `IsDev()`, and `IsProd()`. It suits projects that need only those two environments and want unknown or unset values to default to production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because several local path-like references were unresolved, so the benign verdict has medium confidence.

Mitigation: Review the supplied skill files and resolve the referenced paths before installation; consider the scan incomplete until that review is done.

## Reference(s):

- [Setup and API reference](references/setup.md)
- [goenv project](https://github.com/psyb0t/goenv)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Guidance]

**Output Format:** [Markdown with Go code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides usage examples and API guidance; the library itself writes no files.]

## Skill Version(s):

1.0.12 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
