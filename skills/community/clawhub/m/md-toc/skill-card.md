## Description:

Generate a table of contents for Markdown files by extracting ATX headings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and documentation reviewers use this skill to generate navigable Markdown table-of-contents lists and quickly inspect heading structure before editing or summarizing documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the local Markdown file provided to it and prints extracted headings to stdout.

Mitigation: Run it only on Markdown files the user intended the agent to inspect, and avoid pointing it at sensitive local documents unless that output is acceptable.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown list printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Relative anchor links are derived from ATX headings; the optional --max flag limits heading depth.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
