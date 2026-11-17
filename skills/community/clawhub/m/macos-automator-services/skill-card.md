## Description:

macOS Automator Services helps agents guide users through installing and using five macOS Finder Quick Action workflows for PDF-to-JPG conversion, PNG renaming and conversion, image stitching, RAR extraction, and ordered image renaming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wang-junjian](https://clawhub.ai/user/wang-junjian)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure macOS Finder Quick Actions for recurring file handling tasks such as image conversion, image stitching, RAR extraction, and batch renaming.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release claims to install macOS Automator workflow services, but the artifact does not include the workflow files needed to verify or install those services.

Mitigation: Review the package before installing and proceed only after complete workflow bundles are provided and inspected.

Risk: Deployment and uninstall guidance modifies ~/Library/Services, which controls persistent Finder services.

Mitigation: Back up ~/Library/Services first and remove only workflow bundles confirmed to come from this skill.

Risk: Permission repair guidance includes broad chmod commands over workflow bundles.

Mitigation: Avoid broad permission changes unless needed; inspect ownership and permissions first and apply the least necessary changes.

## Reference(s):

- [Apple Automator User Guide](https://support.apple.com/zh-cn/guide/automator/welcome/mac)
- [Apple Terminal User Guide](https://support.apple.com/zh-cn/guide/terminal/welcome/mac)
- [ImageMagick Documentation](https://imagemagick.org/script/)
- [ImageMagick Command-line Tools](https://imagemagick.org/script/command-line-tools.php)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes macOS/Homebrew setup guidance and Finder service deployment steps.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact changelog, released 2026-03-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
