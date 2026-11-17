## Description:

Scaffold, build, and package SwiftPM-based macOS apps without an Xcode project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dimillian](https://clawhub.ai/user/dimillian)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to bootstrap SwiftPM macOS app projects and generate packaging, signing, notarization, appcast, launch, and development signing guidance outside Xcode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts handle signing credentials and notarization key material.

Mitigation: Review and harden the scripts before release use; replace fixed /tmp key paths with private mktemp directories and restrictive permissions before using App Store Connect credentials.

Risk: The packaging and launch scripts perform destructive cleanup of generated app bundles and running app instances.

Mitigation: Run them from a disposable or version-controlled project copy, and keep APP_NAME to a simple basename before execution.

Risk: version.env is sourced by shell scripts.

Mitigation: Treat version.env as trusted code unless the scripts are changed to parse strict key-value data.

Risk: setup_dev_signing.sh creates a persistent development signing identity in the login Keychain.

Mitigation: Use it only on development machines where that persistent identity is acceptable, and remove the identity from Keychain when it is no longer needed.

## Reference(s):

- [Scaffold a SwiftPM macOS app](references/scaffold.md)
- [Packaging notes](references/packaging.md)
- [Release and notarization notes](references/release.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, code snippets, and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes macOS shell-script templates and SwiftPM project scaffolding guidance; users must provide local app identifiers, signing identities, and optional notarization credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-01-08T09:04:47Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
