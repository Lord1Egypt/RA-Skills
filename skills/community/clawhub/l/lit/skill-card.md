## Description:

文献综述助手 helps researchers search academic literature sources such as arXiv and DBLP from LLM or MCP clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and developers use this skill to query arXiv and DBLP while preparing literature reviews through an agent or MCP client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Literature search queries are sent through XiaoBenYang.

Mitigation: Review query sensitivity before use and avoid sending confidential research or personal data unless the upstream service is approved.

Risk: The skill stores XBY_APIKEY locally in a plaintext .env file.

Mitigation: Use a throwaway or limited-scope API key where possible, keep .env out of source control, and rotate the key if it is exposed.

Risk: The security summary flags mismatched Gaokao naming leftovers in this literature-review release.

Mitigation: Ask the publisher for a cleaned, better-scoped release before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/lit)
- [XiaoBenYang](https://xiaobenyang.com)
- [XiaoBenYang MCP service](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or text summaries derived from JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value; arXiv and DBLP searches accept a query and optional max_results.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
