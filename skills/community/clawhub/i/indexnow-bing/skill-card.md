## Description: <br>
Submits public website URLs and sitemap entries to search engines through the IndexNow protocol to request faster crawling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[domainrankhq](https://clawhub.ai/user/domainrankhq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to generate or reuse an IndexNow key, deploy the required verification file, and submit selected public URLs or sitemap contents for search-engine crawling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit public URLs or sitemap contents to search-engine infrastructure, including URLs that were not intended for indexing. <br>
Mitigation: Review individual URLs and bulk sitemap contents before submission; exclude internal, staging, or otherwise private URLs. <br>
Risk: The generated .indexnow-key file is a sensitive verification credential for URL submission. <br>
Mitigation: Keep .indexnow-key out of version control and shared logs, and deploy only the required public verification file. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/domainrankhq/indexnow-bing) <br>
- [DomainRank AI SEO Skills](https://domainrank.app/ai-seo-skills) <br>
- [IndexNow API Endpoint](https://api.indexnow.org/indexnow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local .indexnow-key file and a public key verification text file when the generate-key command is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
