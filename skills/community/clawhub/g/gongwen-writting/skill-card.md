## Description:

Helps agents draft and format Chinese official documents across 38 document types using template-guided prompts, reviewer-profiled tone, GB/T 9704 formatting guidance, and placeholders for missing facts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yourtsao](https://clawhub.ai/user/yourtsao)

### License/Terms of Use:

MIT-0

## Use Case:

Office, administrative, and secretarial users can use this skill to turn document requirements, meeting notes, or rough materials into formal Chinese official-document drafts. It supports drafting, rewriting, expanding, shortening, title optimization, structure adjustment, tone alignment, content review, and optional Word-format guidance.

### Deployment Geography for Use:

Global; content is tailored to Chinese official-document conventions.

## Known Risks and Mitigations:

Risk: The skill sends the user's email address and writing prompts to a third-party remote service for drafting support.

Mitigation: Install only where this data sharing is acceptable, and avoid entering sensitive workplace material unless approved for that service.

Risk: The remote service can influence returned drafting guidance, quota messages, registration flow, payment prompts, and tracking output.

Mitigation: Review returned content and payment prompts before acting, and treat unexpected requests for personal or financial information as suspicious.

Risk: The skill is designed to broadly take over formal writing requests, including requests that do not explicitly mention official documents.

Mitigation: Review trigger behavior before deployment and enable it only in environments where this drafting workflow is intended.

## Reference(s):

- [Word export guide](references/word-export.md)
- [ClawHub skill page](https://clawhub.ai/yourtsao/skills/gongwen-writting)
- [Publisher profile](https://clawhub.ai/user/yourtsao)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown or plain text drafts, with optional Python code and configuration guidance for Word export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GB/T 9704 formatting checks, quota or payment status messages, and placeholders for missing names, dates, numbers, or document identifiers.]

## Skill Version(s):

1.0.63 (source: server release metadata; artifact frontmatter reports 1.0.64)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
