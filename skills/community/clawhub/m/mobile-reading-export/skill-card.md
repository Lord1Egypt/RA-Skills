## Description:

Turn Markdown or structured documents into mobile-friendly HTML, phone-sized PDFs, and one-page share card images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Document authors and other users prepare long Markdown or structured documents for comfortable phone reading and sharing. The skill helps choose an output format, reflows tables for narrow screens, and checks layout and PDF pagination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chrome rendering runs with the browser sandbox disabled, reducing isolation when opening hostile content.

Mitigation: Render trusted documents in a restricted environment, and avoid processing untrusted HTML or source files with this workflow.

Risk: PDF export may replace an existing file with output that is non-empty but invalid.

Mitigation: Keep a backup and independently open and inspect the replacement PDF before relying on it or discarding the original.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/haiyangchenbj/skills/mobile-reading-export)

## Skill Output:

**Output Type(s):** [HTML, PDF, PNG, Guidance]

**Output Format:** [Responsive HTML, phone-sized PDF, and one-page share card PNG]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [HTML is a single offline file; PDFs use phone-ratio pages; share cards summarize key points.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
