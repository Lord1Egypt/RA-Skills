## Description:

Gigo Lobster Resume provides a legacy-compatible entrypoint for continuing GIGO Lobster benchmark runs; in v2 stable it clears older checkpoints and starts a fresh run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gigolab](https://clawhub.ai/user/gigolab)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to continue or restart interrupted GIGO Lobster benchmark runs and collect the resulting log, report, certificate, and optional shared result link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Benchmark responses, telemetry, and task output may be sent to api.agent-gigo.com.

Mitigation: Run in an isolated workspace or container and use local, offline, or skip-upload mode when a cloud submission is not intended.

Risk: Workspace secrets or private files could be exposed during benchmark execution.

Mitigation: Run from a disposable workspace without secrets.env values, credentials, or private project files.

Risk: Remote evaluation behavior requires trust beyond the resume-focused entrypoint description.

Mitigation: Review the skill, logs, generated report, and upload mode before sharing or relying on benchmark results.

## Reference(s):

- [Gigo Lobster Resume on ClawHub](https://clawhub.ai/gigolab/skills/gigo-lobster-resume)
- [GIGO Lobster Skill Family README](artifact/README.md)
- [GIGO Lobster Taster v2 Bundle README](artifact/bundle/README.md)
- [GIGO Lobster v2 Integration Guide](artifact/bundle/INTEGRATION.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, file paths, and progress updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Points users to gigo-run.log, lobster-report.html, and lobster-cert PNG/SVG outputs.]

## Skill Version(s):

2.1.2 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
