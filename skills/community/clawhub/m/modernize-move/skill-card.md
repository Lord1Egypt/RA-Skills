## Description:

Detects outdated Move V1 syntax, patterns, and APIs and guides agents through tiered Move V2+ modernization with analysis, user confirmation, and test verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iskysun96](https://clawhub.ai/user/iskysun96)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze and modernize legacy Move contracts from V1 patterns to Move V2+ syntax and APIs. It is intended for upgrades and migrations, not for writing new contracts, feature work, bug fixing, gas optimization, or security audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can edit existing Move contracts, and full Tier 3 migrations may introduce ABI, storage, or event-stream breaking changes.

Mitigation: Use it only on a version-controlled project, review the analysis report before approving changes, prefer lower-risk scopes when compatibility matters, and require tests to pass after each approved tier.

Risk: Modernization can preserve syntax while still missing semantic or operational issues outside the skill's scope.

Mitigation: Use the skill for structural migration only, then run separate security review, bug fixing, or gas optimization workflows when those concerns apply.

## Reference(s):

- [Detection Rules](references/detection-rules.md)
- [Transformation Guide](references/transformation-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports with proposed code changes and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation for modernization scope and test verification after each approved tier.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
