## Description:

AI-agent Skill for PPTX OOXML localization workflows. Use it to unpack PPTX, extract and apply text translations, normalize terminology, enforce language-specific fonts, validate XML integrity, and repack outputs with machine-readable JSON interfaces for automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason2be](https://clawhub.ai/user/jason2be)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation agents use this skill to run repeatable PPTX localization workflows: unpacking presentations, extracting text, applying translated TSV content, normalizing terminology and fonts, validating OOXML, and repacking outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted TSV file can steer one write path outside the intended presentation folder.

Mitigation: Process only trusted TSV/job inputs, run workflows on copies in a restricted workspace, and require path containment under the OOXML root before broader deployment.

Risk: Untrusted PPTX, glossary, or job files may cause unwanted changes during automated localization runs.

Mitigation: Review input files before execution and keep workflow outputs isolated from source presentations until validation is complete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jason2be/skills/ppt-ooxml-tool)
- [README](README.md)
- [Release Notes v0.1.0](RELEASE_NOTES_v0.1.0.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-oriented workflow contracts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI workflows can produce TSV, JSON status output, unpacked OOXML files, and repacked PPTX files.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata, pyproject.toml, RELEASE_NOTES_v0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
