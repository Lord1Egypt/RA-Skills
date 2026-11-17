## Description:

Analyzes OpenClaw architecture, identifies pipeline hook points, generates custom hook code, scans code, and produces architecture reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fofo365](https://clawhub.ai/user/fofo365)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to inspect an OpenClaw installation, map its agent pipeline stages and hook points, and generate starter hooks and reports for extension work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated hooks can log complete agent context.

Mitigation: Review generated hook files before enabling them and remove full-context logging or other sensitive data exposure.

Risk: Generated file writes are not clearly scoped.

Mitigation: Validate hook names and output paths, and run the analyzer in a version-controlled or disposable workspace so generated files are easy to inspect and undo.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/fofo365/skills/openclaw-self-analyzer)
- [Artifact skill documentation](artifact/SKILL.md)
- [Generated architecture report](artifact/reports/architecture_report.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, JavaScript hook files, Python API examples, and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates architecture maps, hook manifests, custom hook packages, and human-readable reports.]

## Skill Version(s):

1.0.0 (source: server release metadata and generated hook manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
