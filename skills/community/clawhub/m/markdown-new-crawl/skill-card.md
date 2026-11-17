## Description:

Crawls website sections through markdown.new crawl endpoints and returns page content as Markdown or per-page JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctxinf](https://clawhub.ai/user/ctxinf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to crawl public documentation or public site sections, extract multi-page content, and retrieve the result as Markdown or structured JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs are sent to the external markdown.new service for crawl requests.

Mitigation: Use the skill only for public documentation or public site sections, and do not submit private URLs, authenticated pages, localhost or internal hosts, secrets, or tokenized links.

Risk: Broad crawl settings can increase runtime and service usage.

Mitigation: Keep crawl scope explicit and narrow by setting low limits, depth, include patterns, and exclude patterns for the task.

## Reference(s):

- [markdown.new crawl endpoint](https://markdown.new/crawl)
- [ClawHub skill page](https://clawhub.ai/ctxinf/skills/markdown-new-crawl)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; crawl results are returned as Markdown by default or JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Crawl jobs default to same-domain links, up to 500 pages, and retained results for 14 days according to the skill evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
