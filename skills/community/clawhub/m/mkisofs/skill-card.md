## Description: <br>
Create and manage ISO 9660 images using mkisofs, genisoimage, or xorriso for standard, bootable, UEFI, hybrid, and multi-boot ISO creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidongkl](https://clawhub.ai/user/weidongkl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system engineers use this skill to generate command guidance for creating, inspecting, mounting, extracting, modifying, and validating ISO images, including bootable BIOS, UEFI, hybrid, and multi-boot media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated package installation, mount, extract, overwrite, add, or remove commands can change the local system or ISO contents if run without review. <br>
Mitigation: Require explicit approval before executing those operations, and inspect each generated command before running it. <br>
Risk: Incorrect source, mount, extraction, or output paths can overwrite files or operate on the wrong data. <br>
Mitigation: Confirm all paths and prefer temporary working directories before running ISO creation or modification commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weidongkl/mkisofs) <br>
- [mkisofs manual](https://linux.die.net/man/8/mkisofs) <br>
- [xorriso documentation](https://www.gnu.org/software/xorriso/) <br>
- [ISOLINUX documentation](https://wiki.syslinux.org/wiki/index.php/ISOLINUX) <br>
- [El Torito CD-ROM boot specification](https://en.wikipedia.org/wiki/El_Torito_(CD-ROM_standard)) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
