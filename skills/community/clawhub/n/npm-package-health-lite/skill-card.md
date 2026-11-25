## Description:

Quick health check on an npm package before installing — latest version, days since last publish, deprecation flag, license, and a stale/deprecated heuristic. One unauthenticated registry request. Use when the user asks if an npm package is maintained or safe to add.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nenadzivotic](https://clawhub.ai/user/nenadzivotic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review an npm package's recent publishing activity, deprecation status, and license before deciding whether to add it as a dependency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation command fetches the skill using an unpinned CLI and revision.

Mitigation: Review the source and pin the installer and revision before installing.

Risk: The benign security verdict is based on an incomplete scan, with some components only partially inspected.

Mitigation: Review the skill and its installation source before use; do not treat the verdict as a guarantee of safety.

## Reference(s):

- [ClawHub listing: npm-package-health-lite](https://clawhub.ai/nenadzivotic/skills/npm-package-health-lite)
- [npm registry API](https://registry.npmjs.org/)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [JSON package health summary with a concise recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node 18+; makes one unauthenticated request to the public npm registry.]

## Skill Version(s):

1.1.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
