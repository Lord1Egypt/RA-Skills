## Description:

Runs PII anonymization, local de-anonymization, and deterministic local detector checks for text and supported files for redact/restore flows, file-first anonymization, and offline detector tuning with allowlist, blocklist, and threshold controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modeioai](https://clawhub.ai/user/modeioai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to anonymize text and supported files, restore placeholders from saved maps, and tune deterministic local PII detection with allowlist, blocklist, and threshold controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dynamic, strict, and crossborder modes can send raw sensitive input to a remote or environment-selected API endpoint before redaction.

Mitigation: Use --level lite for local-only processing, or verify ANONYMIZE_API_URL points to a trusted HTTPS backend before using remote-backed modes.

Risk: Saved placeholder map files can restore original PII.

Mitigation: Protect or delete saved map files and set MODEIO_REDACT_MAP_DIR only to storage locations appropriate for sensitive data.

Risk: In-place file modification can overwrite source files during redaction or restoration.

Mitigation: Prefer --output for file workflows and review generated files before replacing originals.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/modeioai/skills/privacy-protector)
- [Publisher Homepage](https://github.com/mode-io/mode-io-skills/tree/main/privacy-protector)
- [Architecture](ARCHITECTURE.md)
- [CLI Contracts](references/cli-contracts.md)
- [File Workflows](references/file-workflows.md)
- [Local Detector](references/local-detector.md)
- [Detect-Local Examples](examples/detect-local/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON-oriented CLI output contracts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce redacted files, sidecar map references, saved placeholder maps, detector diagnostics, and machine-readable JSON envelopes when invoked with --json.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
