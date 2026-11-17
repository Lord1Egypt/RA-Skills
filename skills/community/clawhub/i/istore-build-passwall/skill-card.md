## Description:

Creates and pushes a GitHub Actions workflow that builds PassWall packages for a user's iStoreOS fork.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veelove](https://clawhub.ai/user/veelove)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and router maintainers use this skill to add a PassWall build workflow to an iStoreOS fork, publish build artifacts, and receive instructions for running the generated installer on a router.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for GitHub credentials that may grant broad repository access.

Mitigation: Use a fine-grained, short-lived token scoped to a disposable fork or fresh branch, avoid broad classic PATs, and remove any token from Git configuration after use.

Risk: The workflow setup includes destructive repository changes, including force pushing to the target repository.

Mitigation: Run it only against a disposable fork or branch and confirm the target remote and branch before allowing any push.

Risk: The generated workflow downloads packages and publishes a router installer that may run with elevated privileges on the target device.

Mitigation: Review the workflow, verify downloaded packages and GitHub Actions, and test the installer in a controlled router environment before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/veelove/skills/istore-build-passwall)
- [Build PassWall workflow](artifact/references/build-passwall.yml)
- [iStoreOS repository](https://github.com/istoreos/istoreos)
- [OpenWrt PassWall releases](https://github.com/Openwrt-Passwall/openwrt-passwall/releases)
- [OpenWrt PassWall2 releases](https://github.com/Openwrt-Passwall/openwrt-passwall2/releases)
- [OpenWrt PassWall SourceForge packages](https://sourceforge.net/projects/openwrt-passwall-build/files/releases/packages-22.03)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and a GitHub Actions workflow file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces repository changes and GitHub workflow configuration that can publish router installer artifacts.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
