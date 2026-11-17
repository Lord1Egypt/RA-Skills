## Description:

OmniSearch helps agents retrieve current web information through AI-enhanced or raw search providers and summarize results with citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bguidolim](https://clawhub.ai/user/bguidolim)

### License/Terms of Use:


## Use Case:

Developers and agent operators use OmniSearch to answer requests that require current web, news, price, product, or source-backed factual information. The skill provides a wrapper for AI-enhanced or raw web search and guides the agent to synthesize results with links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may be sent to third-party search or AI-search providers.

Mitigation: Avoid including secrets, private documents, customer data, or confidential workspace details in queries unless that disclosure is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bguidolim/skills/omnisearch)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with source links and optional shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search queries may be routed to external search or AI-search providers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
