## Description:

Reviews pending code changes for common security issues, including secrets exposure, injection, XSS, SSRF, authorization bypass, and vulnerable dependencies, then reports severity and suggested fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code reviewers use this skill before merges, open-source releases, or incident reviews to scan scoped code changes and receive a prioritized security report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read code diffs and surrounding file context that include secrets or sensitive implementation details.

Mitigation: Invoke it with an explicit branch, file list, or commit range when scope matters, and review reports for accidental sensitive disclosure.

Risk: Security fix suggestions can change application behavior or remove legitimate code when applied too broadly.

Mitigation: Require user approval before edits and review proposed patches before merging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-openclaw-security-review)
- [Publisher profile](https://clawhub.ai/user/zhaobod1)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, shell commands, guidance]

**Output Format:** [Markdown security review report with file references, severity ratings, CWE mappings, suggested fixes, and optional shell commands for user-run checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose code changes only after user approval; avoids printing full secrets in reports.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
