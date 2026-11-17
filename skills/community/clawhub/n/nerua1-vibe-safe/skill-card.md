## Description:

Security pre-flight for AI coding agents - plan libraries, audit CVEs, certify, then code, with non-blocking ex-post reporting in autonomous mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerua1](https://clawhub.ai/user/nerua1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI coding-agent users use this skill before introducing external dependencies to plan candidate libraries, check vulnerability and maintenance signals, and produce a dependency safety certificate or post-coding risk report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt an agent to install audit tooling or add commands to PATH without sufficiently scoping trust boundaries.

Mitigation: Require explicit user approval, pinned versions, and reviewed checksums before installing pip-audit or adding any VibeSafe command to PATH.

Risk: Running bundled ./tools scripts from an untrusted project can execute code the user has not reviewed.

Mitigation: Run only a pinned and reviewed release, inspect local scripts before execution, and avoid invoking project-local VibeSafe scripts from repositories you do not trust.

Risk: Dependency audit steps perform network lookups that can disclose package names or project dependency choices to external services.

Mitigation: Confirm network egress is acceptable for the project and avoid sending sensitive private dependency names to public audit APIs unless policy allows it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nerua1/skills/nerua1-vibe-safe)
- [npm audit documentation](https://docs.npmjs.com/cli/v10/commands/npm-audit)
- [pip-audit project](https://pypi.org/project/pip-audit/)
- [OSV.dev query API](https://api.osv.dev/v1/query)
- [deps.dev package API](https://api.deps.dev/v3alpha/packages/npm/${PKGNAME})

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tables and shell command blocks; may direct the agent to create stay_safe.md or risk-report.md outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dependency planning, CVE and maintenance audit results, certification status, and concrete next-step guidance.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
