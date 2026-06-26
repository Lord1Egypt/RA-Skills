## Description: <br>
Scaffold, build, and package SwiftPM-based macOS apps without an Xcode project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dimillian](https://clawhub.ai/user/Dimillian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to bootstrap SwiftPM macOS app projects, assemble .app bundles, run local development builds, and prepare optional signing, notarization, and Sparkle appcast release artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Signing helper scripts handle credentials and modify the user's login keychain. <br>
Mitigation: Review and edit the signing scripts before use, and run setup_dev_signing.sh only when comfortable adding a persistent self-signed signing identity. <br>
Risk: Notarization workflows require App Store Connect credentials and private-key material. <br>
Mitigation: Use a securely created temporary private-key file with restrictive permissions or a safer credential mechanism before providing App Store Connect keys. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Dimillian/macos-spm-app-packaging) <br>
- [Scaffold a SwiftPM macOS app](references/scaffold.md) <br>
- [Packaging notes](references/packaging.md) <br>
- [Release and notarization notes](references/release.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Swift code, configuration examples, and reusable script templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project scaffolding and packaging instructions; generated signing and release scripts should be reviewed and adapted before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
