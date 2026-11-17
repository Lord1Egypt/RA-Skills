## Description:

Extracts PDF AcroForm field schemas and fills forms from user-provided JSON values using a multi-backend fallback chain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qubit999](https://clawhub.ai/user/qubit999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users use this skill to inspect PDF AcroForm fields, build matching JSON values, and produce completed PDF forms in an agent workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned third-party PDF package or optional backends can introduce dependency drift.

Mitigation: Install oc-pdf-filler and its dependencies in a locked environment with pinned versions before production use.

Risk: Input values and filled PDFs may contain personal, financial, medical, legal, or business-sensitive information.

Mitigation: Use the skill only with documents approved for processing in the agent workspace and confirm the attachment destination before delivery.

Risk: PDF backend or viewer differences can cause form appearances to render incorrectly or appear blank.

Mitigation: Verify filled outputs with extraction and visual inspection, and use strict mode, flattening, or a forced backend when needed.

## Reference(s):

- [Field Type Value Contract](artifact/references/FIELD_TYPES.md)
- [Backend Fallback Chain](artifact/references/BACKENDS.md)
- [oc-pdf-filler homepage](https://github.com/qubit999/oc-pdf-filler)
- [Pdf Filler ClawHub page](https://clawhub.ai/qubit999/skills/pdf-filler)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with bash commands, JSON snippets, and generated PDF or JSON workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce filled PDF attachments and JSON summaries; backend behavior depends on installed PDF libraries and optional pdftk.]

## Skill Version(s):

0.1.5 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
