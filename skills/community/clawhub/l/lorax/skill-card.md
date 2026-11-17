## Description:

Lorax helps agents draft guidance and commands for creating bootable Fedora/RHEL ISO, disk, and cloud images with Lorax, livemedia-creator, virt-builder, Kickstart files, and template customizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidongkl](https://clawhub.ai/user/weidongkl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to plan and compose commands and configuration for Fedora/RHEL image builds, including installer ISOs, live media, disk images, cloud images, package selections, boot settings, and Kickstart examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can create images with a known plaintext root password if copied unchanged.

Mitigation: Replace sample credentials with approved secret handling and a strong password policy before building images.

Risk: Package exclusion examples can omit firewall protection from deployable images.

Mitigation: Keep or replace firewall controls intentionally and review package exclusions before use.

Risk: Kickstart disk-wipe directives and cleanup commands can remove data or paths unintentionally.

Mitigation: Scope disk-wipe directives to disposable targets and verify cleanup paths before running recursive deletion commands.

## Reference(s):

- [ClawHub lorax skill page](https://clawhub.ai/weidongkl/skills/lorax)
- [Lorax official documentation](https://github.com/weldr/lorax)
- [Fedora image guide](https://fedoraproject.org/wiki/Fedora_Media_Server)
- [virt-builder documentation](https://libguestfs.org/virt-builder.1.html)
- [Kickstart documentation](https://docs.fedoraproject.org/en-US/fedora/f39/install-guide/install/Kickstart_Syntax_Reference/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; examples should be reviewed and edited before use.]

## Skill Version(s):

1.0.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
