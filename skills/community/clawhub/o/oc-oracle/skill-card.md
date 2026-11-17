## Description:

Oracle CLI second-model review/debug/refactor/design with selected files, dry-run token checks, API or browser engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use Oracle to request a second-model review, debugging help, refactoring suggestions, or design feedback on a selected set of project files. They can preview the prompt and estimated token use before running an API or browser session, and should verify the response against their code and tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install guidance can automatically download and run an unpinned package.

Mitigation: Review the package and installation command before use, and use a pinned package version when available.

Risk: The security scan was partly incomplete because a referenced local path was missing.

Mitigation: Resolve and inspect the missing reference before relying on the scan as a complete assessment.

## Reference(s):

- [Oracle website](https://askoracle.dev)
- [Oracle on ClawHub](https://clawhub.ai/hillstreet-ph/skills/oc-oracle)

## Skill Output:

**Output Type(s):** [Analysis, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory model output; verify recommendations against code and tests.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
