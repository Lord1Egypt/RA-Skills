## Description:

Self-contained operational runbook for verifying ClawHub file endpoint parameter handling. Use when you need a reproducible, benign skill package for endpoint isolation testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lams001](https://clawhub.ai/user/lams001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers can use this runbook to check how ClawHub resolves skill files across paths, versions, tags, and owner handles, and record response status, content type, and cache headers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runbook includes a publication step that can change an externally hosted revision, conflicting with the security summary's read-only assurance.

Mitigation: Review whether publishing is necessary before use. For file-resolution checks, omit the publication step and use a read-only workflow or account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lams001/skills/i45943-fileparam-canary)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown runbook]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
