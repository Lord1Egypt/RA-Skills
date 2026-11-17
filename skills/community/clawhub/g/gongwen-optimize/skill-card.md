## Description:

公文润色 helps agents optimize Chinese official documents, speeches, reports, case materials, and letters by identifying intent, improving structure, sharpening headings, balancing parallel sections, and increasing expression density while avoiding fabricated facts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wing-art](https://clawhub.ai/user/wing-art)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and writing assistants use this skill to polish existing Chinese official or formal organizational drafts such as reports, speeches, requests, replies, case submissions, and letters. It guides the agent to diagnose intent and logic, produce one or more revised versions, and explain the key changes without inventing recipients, real names, positions, or hard data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optimized formal text can still contain inaccurate added background phrasing, policy terms, titles, placeholders, or unsupported implications.

Mitigation: Review outputs for factual accuracy and replace or remove placeholders before using them in real documents.

Risk: The skill can enrich wording and structure, which may blur the line between standard phrasing and unsupported facts if the source draft is thin.

Mitigation: Keep hard data, real names, positions, recipients, and concrete accomplishments limited to information supplied by the user or clearly marked placeholders.

## Reference(s):

- [公文用语规范速查](artifact/references/terminology.md)
- [工作样例](artifact/references/workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown prose with revised drafts, optional variants, and concise change explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output stays in the conversation and does not write files unless explicitly requested.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
