## Description:

Packages H5 game projects into Apple iBook-compatible .wdgt Widget archives, including directory setup, resource path updates, Info.plist generation, thumbnail generation, zip packaging, and validation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onedream1985](https://clawhub.ai/user/onedream1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to prepare interactive H5 projects for legacy Apple iBook Author workflows. It helps create a .wdgt bundle and zip with normalized resources, metadata, thumbnails, and package-structure checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled packing script can delete or package files outside the intended folders when given unsafe paths or symlinked project files.

Mitigation: Run it only on trusted project directories, avoid elevated privileges, review source folders for symlinks, and use a dedicated output directory.

Risk: Unsafe widget names or paths may create confusing or unintended output locations.

Mitigation: Use simple widget names containing only letters, numbers, dashes, and underscores.

Risk: Thumbnail generation may require installing Pillow into the Python environment.

Mitigation: Install Pillow only in a virtual environment when thumbnail generation is needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/onedream1985/skills/ibook-widget-packer)
- [Apple Property List DTD](http://www.apple.com/DTDs/PropertyList-1.0.dtd)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell, HTML, XML, CSS, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create .wdgt folders, Info.plist files, thumbnail PNGs, and .wdgt.zip archives when the bundled script is used.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
