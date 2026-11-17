## Description:

Scans Node.js, Express, Next.js, and React projects for bugs, security issues, frontend hydration problems, configuration gaps, and optional build failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jengajojo](https://clawhub.ai/user/jengajojo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan Node.js web applications for backend, frontend, and configuration issues during debugging, audits, or production preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional build verification can run the target project's npm build script with the user's permissions.

Mitigation: Use --build only for trusted projects, or run it in a disposable sandbox with secrets and network access removed.

Risk: The scanner writes or overwrites AUTO-DEBUG-REPORT.md in the scanned project.

Mitigation: Run it in a working tree where that report path is acceptable, or preserve any existing report before scanning.

## Reference(s):

- [Node Auto Debugger ClawHub Page](https://clawhub.ai/jengajojo/skills/node-auto-debugger)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with severity-grouped findings and inline file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes AUTO-DEBUG-REPORT.md in the scanned project and exits with code 1 when critical findings are detected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
