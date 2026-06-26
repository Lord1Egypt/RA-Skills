## Description: <br>
Runs PII anonymization, local de-anonymization, and deterministic local detector checks for text and supported files. Use for redact/restore flows, file-first anonymization, or offline detector tuning with allowlist, blocklist, and threshold controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modeioai](https://clawhub.ai/user/modeioai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to anonymize sensitive text or supported files, restore placeholders from saved maps, and tune deterministic local detection with allowlists, blocklists, and thresholds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Non-lite anonymization modes send content to an API. <br>
Mitigation: Use --level lite for local-only processing, and use non-lite modes for regulated or confidential data only when the API is approved for that data. <br>
Risk: Restore maps contain original sensitive values on disk. <br>
Mitigation: Store maps only in approved protected locations, control access to the map directory, and override MODEIO_REDACT_MAP_DIR when a dedicated storage path is required. <br>
Risk: PDF workflows are anonymize-only and cannot be restored through the PDF path. <br>
Mitigation: Use supported text-like or DOCX workflows when reversible restore behavior is required, and validate PDF outputs before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/modeioai/privacy-protector) <br>
- [Publisher profile](https://clawhub.ai/user/modeioai) <br>
- [Project homepage](https://github.com/mode-io/mode-io-skills/tree/main/privacy-protector) <br>
- [Architecture](ARCHITECTURE.md) <br>
- [CLI Contracts](references/cli-contracts.md) <br>
- [File Workflows](references/file-workflows.md) <br>
- [Local Detector](references/local-detector.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON envelopes, local configuration files, and redacted or restored file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local lite mode, API-backed non-lite modes, sidecar or embedded restore map references, and machine-readable --json output.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
