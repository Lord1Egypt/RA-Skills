## Description:

Export HTML presentations to editable PPTX slides using pure Python without browser dependencies, ideal for sandbox environments and limited runtimes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaisersong](https://clawhub.ai/user/kaisersong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert HTML slide decks into editable PowerPoint files when browser-based renderers such as Playwright or Chrome are unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime dependency installation can fetch mutable packages during execution.

Mitigation: Preinstall pinned dependencies in a controlled environment and disable runtime auto-install where possible.

Risk: HTML image sources can reference file paths, relative paths, or remote URLs from the machine running the exporter.

Mitigation: Export only trusted HTML, restrict local filesystem and network access, and review or remove untrusted image references before running the skill.

Risk: Untrusted HTML may produce misleading or incomplete slide output because JavaScript is not executed and layout is approximated without a browser.

Mitigation: Review generated PPTX files before use and prefer known input decks or validated templates for production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaisersong/skills/kai-export-ppt-lite)
- [README](README.md)
- [Release notes](RELEASE.md)
- [Skill entrypoint](SKILL.md)
- [Export hints schema](contracts/export_hints.schema.json)
- [Slide creator manifest](contracts/slide_creator/manifest.json)

## Skill Output:

**Output Type(s):** [files, shell commands, configuration, guidance]

**Output Format:** [PPTX files, optional PNG previews, and Markdown command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces editable PowerPoint elements from parsed HTML/CSS; fidelity is semantic rather than pixel-perfect because no browser layout engine is used.]

## Skill Version(s):

1.6.9 (source: server release, SKILL.md frontmatter, README, RELEASE.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
