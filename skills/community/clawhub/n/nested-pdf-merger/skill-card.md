## Description:

Merges PDFs from nested directory trees into a single PDF with hierarchical bookmarks by invoking the external `nestedpdfmerger` CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyutenant](https://clawhub.ai/user/lyutenant)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and document workflow operators use this skill to merge PDFs from nested folder trees, preserve hierarchy as bookmarks, preview merge order, and choose merge options through the `nestedpdfmerger` CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing an unpinned external `nestedpdfmerger` package.

Mitigation: Install the dependency only from a trusted package source, preferably in a virtual environment, and pin a reviewed `nestedpdfmerger` version before using it on sensitive PDFs.

Risk: Sensitive PDFs are processed by an external CLI dependency.

Mitigation: Review the installed CLI and run it only in trusted environments before processing confidential documents.

## Reference(s):

- [Nested PDF Merger homepage](https://github.com/Lyutenant/nested-pdf-merger)
- [ClawHub skill page](https://clawhub.ai/lyutenant/skills/nested-pdf-merger)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces proposed CLI invocations and usage guidance; merged PDF files are produced by the external `nestedpdfmerger` command.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
