## Description:

Find, verify, and analyze papers published in Nature Machine Intelligence (NMI) using official Nature and Springer Nature sources. Use for NMI paper searches by year, topic, author, or method; paper summaries; comparisons; topic trends; and citation or related-work exploration. By default, use items labeled Article in the NMI archive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leogoat2004](https://clawhub.ai/user/leogoat2004)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers use the skill to find Nature Machine Intelligence papers and produce sourced summaries, comparisons, related-work connections, and carefully scoped topic trends. It helps users distinguish publisher-verified facts from synthesis and state when access is limited to an abstract or metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Springer Nature API searches send the user's query to the publisher and consume API quota.

Mitigation: Use the API only when helpful; use the official NMI archive without an API key when appropriate, and avoid sending sensitive query terms.

Risk: API credentials could be exposed if key-bearing request URLs appear in logs or chat.

Mitigation: Keep SN_API_KEY in the process environment and keep key-bearing URLs out of logs and chat.

## Reference(s):

- [NMI article archive](https://www.nature.com/natmachintell/articles)
- [NMI content types](https://www.nature.com/natmachintell/content)
- [Springer Nature Meta API documentation](https://dev.springernature.com/docs/api-endpoints/meta-api/)
- [Springer Nature API key authentication](https://dev.springernature.com/docs/quick-start/authentication/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with paper links, citations, and tables when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides concise literature summaries, comparisons, related-work connections, and scoped topic syntheses; states evidence and access limits.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
