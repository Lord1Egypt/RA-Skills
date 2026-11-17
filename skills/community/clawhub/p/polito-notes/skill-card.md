## Description:

Convert PDF lecture slides into comprehensive bilingual Italian and English markdown notes for Polito university courses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lookupmark](https://clawhub.ai/user/lookupmark)

### License/Terms of Use:

MIT-0

## Use Case:

Students or course-note maintainers use this skill to turn a PDF lecture deck into paired Italian and English markdown notes, organized under the matching Polito course folder. It is intended for lecture material where preserving detailed source content is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF contents may include personal, confidential, unpublished, or regulated information that would be preserved in generated plaintext notes and backups.

Mitigation: Use the skill only with lecture material suitable for plaintext storage, and add a review, redaction, or confirmation step before writing notes for sensitive PDFs.

Risk: Generated notes may be picked up by local RAG indexing, making extracted PDF content searchable beyond the immediate note-generation workflow.

Mitigation: Disable or scope local indexing for sensitive course folders, or keep sensitive generated notes outside indexed paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lookupmark/skills/polito-notes)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Bilingual markdown note files with matching section structure, plus a concise completion summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Italian notes.md and English notes-en.md, creates backups before overwriting existing notes, and may leave generated plaintext notes available for local indexing.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
