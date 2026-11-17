## Description:

Ifeng helps an agent search and summarize public Phoenix News pages, including keyword news collections, channel trends, and article key points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codenova58](https://clawhub.ai/user/codenova58)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and agent users use this skill for lightweight monitoring and summarization of publicly available Phoenix News articles and channel pages. Typical tasks include keyword news summaries, channel hot-topic statistics, and long-form article key point extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heavy or automated use could conflict with Phoenix News site terms or create unwanted bulk collection behavior.

Mitigation: Review site terms, keep usage light, avoid bulk collection, and do not reverse engineer platform interfaces.

Risk: Summaries of public news pages may omit context or reflect source-page errors.

Mitigation: Include source links and collection time in outputs so users can verify important claims against the original pages.

## Reference(s):

- [Phoenix News homepage](https://www.ifeng.com/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries and structured lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source links, collection time, and publicly displayed metadata when available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
