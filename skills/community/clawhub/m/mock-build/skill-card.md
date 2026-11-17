## Description:

Guides agents through managing reproducible RPM package builds with Mock in clean chroot environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidongkl](https://clawhub.ai/user/weidongkl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and build engineers use this skill to set up Mock, choose RPM build presets, run SRPM and spec builds, manage chroot environments, configure plugins, and troubleshoot build results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent passwordless Mock privileges and broad mock group membership can expand host-level access on build machines.

Mitigation: Use a dedicated or disposable build machine, avoid the passwordless sudoers entry, and limit mock group membership to trusted users.

Risk: Insecure build settings such as disabled RPM signature checks or unnecessary build networking can weaken supply-chain protections.

Mitigation: Keep RPM signature verification enabled and disable build networking unless a specific trusted build process requires it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weidongkl/skills/mock-build)
- [Mock official documentation](https://rpm-software-management.github.io/mock/)
- [Fedora Mock build guide](https://docs.fedoraproject.org/en-US/quick-docs/mock/)
- [Mock plugin documentation](https://rpm-software-management.github.io/mock/plugins.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English guidance with RPM build examples]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
