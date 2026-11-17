## Description:

Intelligently splits long academic or technical documents into chapters, generates structured JSON summaries for each, and creates a file system with a global index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrchenkuan](https://clawhub.ai/user/mrchenkuan)

### License/Terms of Use:


## Use Case:

Developers, researchers, and document analysts use this skill to turn long papers, reports, books, or technical documents into chapter files, structured summaries, and a master index for retrieval and follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled scripts contain hard-coded personal input and output paths, which can fail outside the publisher's environment or process unintended local files.

Mitigation: Review the skill before installing, use it only in a controlled workspace, and replace hard-coded paths with explicit user-approved input and output paths.

Risk: Security evidence states that bundled scripts do not match the advertised workflow, so generated outputs may be incomplete relative to the skill description.

Mitigation: Validate behavior on non-sensitive sample documents before relying on generated chapter files, JSON summaries, or index files.

Risk: The skill is designed to persist extracted document content locally, which may be inappropriate for confidential, regulated, or unpublished documents.

Mitigation: Avoid running the skill on sensitive documents unless local persistence of extracted content has been approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrchenkuan/skills/large-document-reader)
- [Publisher profile](https://clawhub.ai/user/mrchenkuan)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, code, shell commands, guidance]

**Output Format:** [Markdown guidance with generated chapter Markdown files, JSON summaries, and a master index.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a reusable document structure intended for overview-first retrieval and chapter-level deep dives.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
