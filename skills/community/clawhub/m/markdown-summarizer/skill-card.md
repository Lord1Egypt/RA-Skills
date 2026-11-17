## Description:

Summarize long markdown documents into structured key-point summaries. Use when a user pastes or points to a long markdown file and wants a concise structured summary with main sections, key findings, and action items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to condense long markdown files, meeting notes, design documents, or articles into a structured overview, key points, section details, and action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive content when users provide private markdown documents.

Mitigation: Avoid giving it confidential documents unless that content is approved for processing in the current agent session.

Risk: Summaries can omit nuance or misstate the emphasis of the original document.

Mitigation: Review the generated summary against the source markdown before relying on it for decisions or publication.

## Reference(s):

- [Summary Template Reference](references/summary-template.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown structured summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summary is normally kept under 20% of the original document length unless a detailed summary is requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
