## Description: <br>
Uses markdown.new crawl endpoints to recursively crawl a site section and return Markdown, including async job creation, status polling, and optional JSON page records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ctxinf](https://clawhub.ai/user/ctxinf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to crawl public websites or documentation sections and convert the pages into Markdown while controlling crawl scope, polling async jobs, and falling back when the crawl endpoint is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private or sensitive URLs may be processed and retained by markdown.new. <br>
Mitigation: Use this skill for public websites or documentation where third-party processing is acceptable; avoid intranet pages, localhost URLs, authenticated content, presigned links, confidential documents, and URLs containing tokens unless that processing is acceptable. <br>
Risk: Overly broad crawls can consume quota and increase runtime. <br>
Mitigation: Set explicit limits, depth, include and exclude patterns, and external-link or subdomain options before starting a crawl. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ctxinf/markdown-new-crawl) <br>
- [markdown.new crawl endpoint](https://markdown.new/crawl) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON crawl results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Crawl output is Markdown by default, with per-page JSON available when requested; artifact evidence states results are retained for 14 days.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
