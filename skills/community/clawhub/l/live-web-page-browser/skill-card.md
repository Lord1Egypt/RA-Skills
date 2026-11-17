## Description:

Fetch live webpages and return HTML, Markdown, structured data, links, screenshots, PDFs, or crawl results through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to retrieve and inspect live webpages for research, content verification, and visual documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's seven-day freshness rule may lead to replacing installed instructions without a clear user review step.

Mitigation: Require approval before installing dependencies or replacing the skill, and review fixed versions of the installer and downloaded instructions.

Risk: URLs and extraction prompts may contain confidential information, and unbounded crawl activity may increase usage.

Mitigation: Set an AgentPMT spending limit, bound crawl size, and avoid confidential URLs or extraction prompts unless provider processing is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/live-web-page-browser)
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/live-web-page-browser)

## Skill Output:

**Output Type(s):** [HTML, Markdown, JSON, Links, Screenshots, PDFs, Crawl results]

**Output Format:** [HTML, Markdown, JSON, links, screenshots, PDFs, and structured crawl results, depending on the selected action]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Crawl actions return job identifiers and results are retrieved asynchronously.]

## Skill Version(s):

1.0.2 (source: frontmatter; confirmed by server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
