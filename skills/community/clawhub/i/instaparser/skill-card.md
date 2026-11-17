## Description:

Use the Instaparser API to parse articles, PDFs, and generate summaries from URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donohue](https://clawhub.ai/user/donohue)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract article or PDF content and request summaries through the Instaparser service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected URLs, HTML content, or PDFs to the external Instaparser service.

Mitigation: Use it only for content intended for external processing and confirm Instaparser's terms and data handling before uploading confidential documents.

Risk: The skill requires an Instaparser API key.

Mitigation: Set INSTAPARSER_API_KEY through an environment variable or secret store instead of pasting credentials into chat.

Risk: Parsing and summary requests may consume account credits or hit service limits.

Mitigation: Review request scope before execution and monitor Instaparser account usage, rate limits, and plan limits.

## Reference(s):

- [ClawHub Instaparser Skill Page](https://clawhub.ai/donohue/skills/instaparser)
- [Instaparser Website](https://www.instaparser.com)
- [Instaparser API Base](https://www.instaparser.com/api/)
- [Instaparser Article API](https://www.instaparser.com/api/1/article)
- [Instaparser PDF API](https://www.instaparser.com/api/1/pdf)
- [Instaparser Summary API](https://www.instaparser.com/api/1/summary)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Markdown, Guidance]

**Output Format:** [Markdown with inline shell commands and parsed API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and INSTAPARSER_API_KEY; API use may consume Instaparser credits.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
