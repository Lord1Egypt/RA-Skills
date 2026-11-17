## Description:

Fetches hot or recommended articles from QbitAI, 人人都是产品经理, and Huxiu, then formats the results as concise Markdown links for IT, technology, internet, AI, product, and business technology news requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengzuo613](https://clawhub.ai/user/zengzuo613)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve current popular IT, technology, AI, product, and business technology articles from three named Chinese news and product sites. It is intended for concise title-and-link news digests rather than search-engine aggregation or article summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run for broad tech-news prompts and open three named external websites in a visible browser.

Mitigation: Use the skill for specific hot or recommended article requests and review whether access to the named external sites is acceptable in the deployment environment.

Risk: Homepage structure changes or missing article links can make a source block incomplete.

Mitigation: Treat incomplete retrievals as failures for that source and require confirmed titles with direct article links before presenting final results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zengzuo613/skills/hot-it-news)
- [QbitAI](https://www.qbitai.com/)
- [人人都是产品经理](https://www.woshipm.com/)
- [Huxiu](https://www.huxiu.com/)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown list of article titles and links grouped by source site]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normally returns up to five linked articles per configured source when source blocks and article links are confirmed.]

## Skill Version(s):

1.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
