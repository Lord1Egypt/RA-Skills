## Description:

Create and manage ISO 9660 images using mkisofs, genisoimage, or xorriso for standard, bootable, UEFI, hybrid, and multi-boot ISO creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weidongkl](https://clawhub.ai/user/weidongkl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and build engineers use this skill to ask an agent for ISO image creation, boot configuration, image inspection, mounting, extraction, modification, and verification guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated file, mount, and image-modification commands can write to unintended paths or alter ISO contents if run without review.

Mitigation: Review output paths and target files before execution, prefer a test directory, and use read-only mounts unless modification is intentional.

## Reference(s):

- [mkisofs Manual](https://linux.die.net/man/8/mkisofs)
- [xorriso Documentation](https://www.gnu.org/software/xorriso/)
- [ISOLINUX Documentation](https://wiki.syslinux.org/wiki/index.php/ISOLINUX)
- [El Torito Specification](https://en.wikipedia.org/wiki/El_Torito_(CD-ROM_standard))

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples, configuration snippets, and command-reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese/English content; users should review output paths, mount targets, and image-modification commands before execution.]

## Skill Version(s):

1.0.1 (source: evidence release metadata and package.json; artifact/SKILL.md changelog lists v1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
