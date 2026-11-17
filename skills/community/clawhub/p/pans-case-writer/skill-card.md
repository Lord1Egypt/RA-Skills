## Description:

Packages customer success information into structured case studies with a background, challenge, solution, and results template, then exports Markdown, HTML, or PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn customer success details into structured case-study narratives and export them for sales, marketing, or customer-story workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF export from untrusted Markdown may trigger local or network resource access during rendering.

Mitigation: Export only trusted Markdown, or run exports in a sandbox without sensitive local files or unrestricted network access.

Risk: HTML export preserves raw markup from input files.

Mitigation: Sanitize untrusted Markdown before HTML export and review generated HTML before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dashiming/skills/pans-case-writer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown case-study drafts, HTML/PDF exports, and CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated case-study files may be written under the user's local case directory; HTML and PDF export should be limited to trusted Markdown.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
