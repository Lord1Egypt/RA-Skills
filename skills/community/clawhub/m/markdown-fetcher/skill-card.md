## Description: <br>
Converts public webpage content into readable Markdown using prioritized conversion services and an optional Scrapling fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jiaqi-Guo-0114](https://clawhub.ai/user/Jiaqi-Guo-0114) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to fetch public webpages and convert articles or web data into Markdown for reading, analysis, or note-taking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URLs are sent to named third-party conversion services. <br>
Mitigation: Use this skill for public webpages; avoid private intranet links, authenticated pages, confidential targets, and URLs containing tokens or secrets unless those services are approved for the data. <br>
Risk: The optional fallback depends on installing and running Scrapling locally. <br>
Mitigation: Review the Scrapling package before installing or using the fallback. <br>


## Reference(s): <br>
- [Markdown Fetcher on ClawHub](https://clawhub.ai/Jiaqi-Guo-0114/markdown-fetcher) <br>
- [markdown.new](https://markdown.new/) <br>
- [defuddle.md](https://defuddle.md/) <br>
- [r.jina.ai](https://r.jina.ai/) <br>
- [Scrapling](https://github.com/D4Vinci/Scrapling) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with service URLs and optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prioritizes markdown.new, defuddle.md, r.jina.ai, then Scrapling as a local fallback.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
