## Description:

Compares revised outline, script, treatment, beat sheet, season map, or character-bio PDFs against older DOCX/PDF baselines and produces a structural-change report plus visible PDF markup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hshgogogo](https://clawhub.ai/user/hshgogogo)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, story editors, and agents use this skill to compare revised story documents against older baselines and mark only structural additions or rewrites. It is suited for bilingual workflows where visible PDF margin notes and companion Markdown/DOCX reports are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft content is extracted and duplicated into local plaintext, JSON, PDF, Markdown, and DOCX outputs.

Mitigation: Use the skill only on drafts that are approved for local duplication and handle generated outputs according to the user's data policy.

Risk: The auto-follow workflow can overwrite prior comparison files when output paths are reused.

Mitigation: Review output directories and filenames before rendering, and preserve prior comparison outputs when needed.

Risk: Dependency drift can affect local extraction or rendering behavior.

Mitigation: Install the skill in a dedicated virtual environment and pin dependencies when repeatability matters.

## Reference(s):

- [macOS Workflow](references/macos.md)
- [Windows Workflow](references/windows.md)
- [Manifest Schema](references/manifest-schema.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report, DOCX report, JSON annotation manifest, and annotated PDF with visible margin notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local comparison artifacts and a normalized annotation manifest; no API calls or external services are required by the artifact evidence.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
