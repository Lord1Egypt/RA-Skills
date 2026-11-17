## Description:

Convert multi-page PDFs into a single vertical long image by concatenating all pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pe-evolver](https://clawhub.ai/user/pe-evolver)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert a local multi-page PDF into one vertical PNG for sharing, review, or visual summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted or extremely large PDFs, or high render scale values, can increase resource usage during conversion.

Mitigation: Run the skill in an isolated Python environment, avoid untrusted or extremely large PDFs, and keep scale values conservative.

Risk: Unpinned dependencies can reduce reproducibility or make dependency updates harder to review.

Mitigation: Prefer pinned versions of PyMuPDF and Pillow when reproducibility or deployment control matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pe-evolver/skills/pdf2image)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files]

**Output Format:** [Markdown guidance with inline bash commands; generated output is a PNG image file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a PDF input path, optional output path, and optional render scale; large PDFs or high scale values can increase memory and disk use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
