## Description:

Create, parse, and edit ODT (OpenDocument Text) files locally using Python and odfdo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juicyroots](https://clawhub.ai/user/juicyroots)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect, create, extract text from, and modify local ODT documents, including append, replace, metadata, font, outline, and style operations. It can be paired with a separate NextCloud skill when document download or upload is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation uses an unpinned odfdo package, which can change behavior across versions.

Mitigation: Install dependencies in a virtual environment and prefer pinned, reviewed package versions.

Risk: NextCloud examples involve a separate skill that can download or upload files outside this local editor's boundary.

Mitigation: Use the NextCloud workflow only when remote document transfer is intended, and review the target paths before upload or download.

Risk: Document edits can overwrite local ODT files if commands are run against the wrong path.

Mitigation: Inspect unfamiliar documents first and work from temporary or backup copies before saving final edits.

## Reference(s):

- [ODT File Manager Reference](artifact/REFERENCE.md)
- [ClawHub Skill Page](https://clawhub.ai/juicyroots/skills/odt-filemgr-oc)
- [Publisher Profile](https://clawhub.ai/user/juicyroots)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, Python snippets, plain-text extraction, JSON metadata output, and modified ODT files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.10+ and odfdo; ODT file changes are local unless a separate NextCloud skill is used for transfer.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
