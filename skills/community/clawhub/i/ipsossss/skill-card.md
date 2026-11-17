## Description:

This skill fills Word documents from authoritative Excel, XLS, or CSV data while preserving the supplied Word template's structure and formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[libanzheng](https://clawhub.ai/user/libanzheng)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users use this skill to fill Word templates from authoritative Excel or CSV data while preserving target document structure and reference formatting. It supports grounded drafting, source mapping, and semantic and visual checks before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsupported fields may be filled with the Chinese placeholder `待确认`, which may not be acceptable in every document.

Mitigation: Confirm the preferred unsupported-field marker before use, or instruct the agent to leave unsupported fields blank.

Risk: The skill references `references/grounding-and-qa.md`, but the packaged artifact does not include that file.

Mitigation: Review source mapping, factual claims, and rendered document output carefully before relying on the generated Word document.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, Text, Guidance]

**Output Format:** [Filled DOCX document with concise Markdown handoff]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May identify fields left blank or marked for confirmation when source support is missing.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
