## Description: <br>
Crawl any website and save pages as local markdown files. Ideal for downloading documentation, knowledge bases, or web content for offline access or analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthew77](https://clawhub.ai/user/matthew77) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to crawl public or authorized websites, collect documentation and knowledge base content, and save or print extracted pages for offline analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crawling unauthorized, internal, authenticated, confidential, or regulated content may send sensitive information to Tavily. <br>
Mitigation: Use the skill only for sites you are authorized to crawl, and avoid sensitive content unless organizational policy permits sending it to Tavily. <br>
Risk: Broad crawls can collect more content than intended or create large local outputs. <br>
Mitigation: Use conservative depth and page limits, path filters, and a dedicated output directory. <br>
Risk: Crawled web content may be untrusted when reused as agent context. <br>
Mitigation: Review crawled content before relying on it or feeding it into an agent. <br>
Risk: The Tavily API key can authorize external crawl requests if exposed. <br>
Mitigation: Use a revocable Tavily API key and rotate it if it may have been disclosed. <br>


## Reference(s): <br>
- [Tavily](https://tavily.com) <br>
- [ClawHub skill page](https://clawhub.ai/matthew77/liang-tavily-crawl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, files, shell commands, configuration] <br>
**Output Format:** [Markdown or JSON crawl results, with optional local markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; supports crawl depth, breadth, page limit, output directory, path filters, instructions, chunking, timeout, and JSON output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
