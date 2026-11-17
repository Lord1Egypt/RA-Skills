## Description:

文献助手 helps users find academic literature with bilingual search terms and analyze one uploaded PDF with grounded summaries and question answering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyt0302](https://clawhub.ai/user/lyt0302)

### License/Terms of Use:

MIT-0

## Use Case:

External users and researchers use this skill to discover academic papers by topic, author, keyword, or recent time range, with Chinese and English search terms. They can also upload a single PDF for structured extraction, Chinese summary, and document-grounded question answering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Literature results can be misleading if paper links, source details, or full-text availability are assumed rather than confirmed.

Mitigation: Return source links and explicit availability labels, and mark access as unconfirmed when full-text availability is not verified.

Risk: PDF question answering can overstate information that is not present in the uploaded document.

Mitigation: Answer primarily from the PDF and state clearly when an answer is not found in the document.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lyt0302/skills/literature-helper)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured sections and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes bilingual search terms, paper metadata, availability labels, PDF summaries, extracted findings, limitations, and answers grounded in the uploaded PDF.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
