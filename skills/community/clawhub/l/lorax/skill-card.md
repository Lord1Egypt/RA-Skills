## Description: <br>
Create bootable Fedora and RHEL system images, including ISO, disk, and cloud images, with Lorax-focused package, template, and boot configuration guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidongkl](https://clawhub.ai/user/weidongkl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, release engineers, and system image maintainers use this skill for guidance on building Fedora/RHEL installer ISOs, live media, disk images, and cloud images with Lorax, livemedia-creator, virt-builder, Kickstart, and related configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sample Kickstart content includes a plaintext root password. <br>
Mitigation: Lock the root account or replace the sample with a strong hashed password before use. <br>
Risk: Sample partitioning uses destructive disk clearing during installation. <br>
Mitigation: Review and target Kickstart partitioning carefully, and test image builds in a disposable VM or build host. <br>
Risk: Cleanup examples delete files under the Lorax temporary directory. <br>
Mitigation: Verify cleanup paths before running deletion commands. <br>


## Reference(s): <br>
- [Lorax Official Docs](https://github.com/weldr/lorax) <br>
- [Fedora Image Guide](https://fedoraproject.org/wiki/Fedora_Media_Server) <br>
- [virt-builder Docs](https://libguestfs.org/virt-builder.1.html) <br>
- [Kickstart Docs](https://docs.fedoraproject.org/en-US/fedora/f39/install-guide/install/Kickstart_Syntax_Reference/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese and English guidance with command references, Kickstart examples, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
