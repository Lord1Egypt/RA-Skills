## Description:

Async/await error handling auditor that scans JavaScript, TypeScript, Python, and Go code for unhandled async errors, including floating promises, async route handlers without error handling, Promise.all calls without an error boundary, asyncio task exceptions, ignored goroutine errors, and missing Node.js unhandledRejection listeners.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit async error handling before production deployment or CI release gates. It reports suspected async reliability issues and suggested fixes for JavaScript, TypeScript, Python, and Go projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scans local project source files.

Mitigation: Run it only in workspaces where local static analysis is acceptable.

Risk: Static analysis findings can be false positives or incomplete.

Mitigation: Review each reported finding and suggested fix before applying code changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-async-audit)
- [Canlah AI homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown report with findings, severities, matched code snippets, suggested fixes, and optional CI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill reports findings from a local static scan and does not modify source files.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
