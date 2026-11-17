## Description:

Crawl any website and save pages as local markdown files. Ideal for downloading documentation, knowledge bases, or web content for offline access or analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthew77](https://clawhub.ai/user/matthew77)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to crawl public websites, documentation, and knowledge bases, then review the returned content or save pages locally for offline analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crawl URLs and natural language instructions are sent to Tavily using the user's API key.

Mitigation: Avoid crawling sensitive internal or proprietary sites without approval.

Risk: Broad crawl settings can collect and save more local content than intended.

Mitigation: Use conservative depth and limit values, and apply select or exclude path filters for focused crawls.

## Reference(s):

- [Tavily](https://tavily.com)
- [Tavily Crawl API endpoint](https://api.tavily.com/crawl)
- [ClawHub skill page](https://clawhub.ai/matthew77/skills/liang-tavily-crawl)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Configuration]

**Output Format:** [Markdown crawl results, raw JSON when requested, or local Markdown files when an output directory is provided.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY. Supports crawl depth, breadth, page limits, path filters, semantic instructions, chunk counts, timeout, JSON output, and local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
