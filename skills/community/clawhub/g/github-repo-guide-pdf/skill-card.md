## Description:

Analyze a GitHub repository URL or OWNER/REPO and produce a Chinese user guide focused on how to use the project, not how it is implemented.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smile618](https://clawhub.ai/user/smile618)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users use this skill to turn a GitHub repository into a usage-first Chinese Markdown guide and PDF manual. It is intended for repository introductions, quick starts, tutorials, and user guides rather than implementation analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF generation processes Markdown with raw TeX enabled, which can create local file or resource exposure risks.

Mitigation: Run PDF generation in a restricted workspace without sensitive files or credentials, and disable or sanitize raw TeX unless the input is trusted.

Risk: Processing untrusted repositories may incorporate misleading or unsafe project instructions into the generated guide.

Mitigation: Review the generated Markdown and PDF before sharing or following the guide, especially for repositories from unknown publishers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smile618/skills/github-repo-guide-pdf)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Chinese Markdown guide, generated PDF, and MEDIA lines identifying the produced files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written under the workspace media directory with timestamped Markdown and PDF filenames.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
