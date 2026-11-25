## Description:

Convert Markdown articles into LinkedIn-ready rich text HTML, preserving supported formatting and handling tables as lists or images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and writers use this skill to prepare Markdown drafts for LinkedIn's article editor while preserving formatting and choosing how tables and images should appear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Table image rendering may expose untrusted HTML to Chromium without the browser sandbox.

Mitigation: Use table flattening for Markdown that may contain untrusted HTML, and review the article before conversion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/j3ffyang/skills/md-to-linkedin)

## Skill Output:

**Output Type(s):** [HTML, Files]

**Output Format:** [HTML fragment and HTML file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The HTML can include embedded images; optional modes produce table PNGs or a DOCX file.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
