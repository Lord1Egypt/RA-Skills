## Description:

Guides agents through diagnosing failed macOS Xcode Command Line Tools installs, resolving Apple sucatalog package URLs, downloading CLT packages through terminal proxy settings, verifying package signatures, and preparing a user-run installer script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isxiaojian](https://clawhub.ai/user/isxiaojian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical support agents use this skill when macOS Command Line Tools installation fails through the GUI, xcode-select, or softwareupdate. It helps produce diagnostic commands, Apple package download URLs, signature-checking steps, and a local installer script that the user runs manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated installer uses administrator privileges after a weak signature check.

Mitigation: Review the generated install script before running it and independently confirm each package signer is Apple Software or Software Signing before entering an administrator password.

Risk: Downloading or installing packages from an untrusted location could compromise the offline installation flow.

Mitigation: Download packages only from Apple catalog URLs and keep the package directory private.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/isxiaojian/skills/macos-clt-offline-install)
- [Apple software update catalog for macOS 15](https://swscan.apple.com/content/catalogs/others/index-15-14-13-12-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog)
- [Apple software update catalog for macOS 14](https://swscan.apple.com/content/catalogs/others/index-14-13-12-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog)
- [Apple software update catalog for macOS 13](https://swscan.apple.com/content/catalogs/others/index-13-12-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash commands and generated shell script content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Apple package URLs and a local installer script; installation requires user review and administrator approval outside the agent sandbox.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
