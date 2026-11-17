## Description:

Splits PDF files into single pages or selected page ranges, with batch workflows and custom output prefixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fly3094](https://clawhub.ai/user/fly3094)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to split local PDF documents into per-page files or selected page-range files without uploading the documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes generated PDFs to a user-selected output directory.

Mitigation: Run it only on PDFs intended for processing and choose output paths deliberately to avoid cluttering or overwriting expected locations.

Risk: The release depends on the Node package pdf-lib, and the evidence does not include a lockfile.

Mitigation: Pin pdf-lib or use a lockfile before deployment.

## Reference(s):

- [PDF Split on ClawHub](https://clawhub.ai/fly3094/skills/pdf-split)
- [fly3094 publisher profile](https://clawhub.ai/user/fly3094)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PDF files written locally, with console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and pdf-lib; outputs single-page PDFs or selected page-range PDFs to a chosen directory.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
