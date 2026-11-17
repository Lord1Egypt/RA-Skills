## Description:

Builds and packages Flutter Android release artifacts (APK/AAB), collects outputs into a single folder, and produces a short release checklist for app release preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neo1307](https://clawhub.ai/user/neo1307)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to build Flutter Android APK or AAB release outputs, gather mapping and manifest artifacts, and produce a concise checklist for Play Store or sharing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may run a local PowerShell release script with ExecutionPolicy Bypass.

Mitigation: Confirm scripts/flutter_release.ps1 is trusted before execution and review generated commands before running them.

Risk: Generated APK/AAB, mapping, and symbol files can contain release-sensitive information.

Mitigation: Share collected release artifacts only with intended recipients and handle mapping/symbol files as sensitive release materials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neo1307/skills/neo1307-flutter-release-pipeline)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline PowerShell and Flutter shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include APK/AAB file paths, file sizes, SHA256 hashes, and a release checklist.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
