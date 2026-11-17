## Description:

Rename academic PDF papers to a standardized format "[Year] [Venue] Title.pdf" using a three-stage Extract, Verify, and Rename pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[67available](https://clawhub.ai/user/67available)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and document-library maintainers use this skill to organize folders of academic PDFs by extracting first-page text, verifying bibliographic metadata, previewing proposed filenames, and executing batch renames when entries are confirmed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled stale manifests and folder-specific helper data can drive incorrect renames or moves against user-accessible files.

Mitigation: Remove bundled manifest files and folder-specific VERIFIED_DATA helpers, regenerate the manifest for the exact target folder, and run preview before execution.

Risk: Executing the rename stage changes files on disk and may be hard to reverse if metadata is wrong.

Mitigation: Use a disposable copy of the PDF folder, inspect the preview, and run --execute only after confirmed metadata matches the intended files.

Risk: Optional LLM parsing sends extracted PDF text to the configured local gateway, which may expose confidential document contents.

Mitigation: Avoid the LLM parsing path for confidential PDFs unless the gateway and data handling are approved for that content.

## Reference(s):

- [Manifest Schema](references/manifest_spec.md)
- [Standard Venue Abbreviations](references/venue_abbrev.md)
- [Common Mistakes and Anti-patterns](references/anti_patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python data snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces manifests and rename previews before optional file-moving execution.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
