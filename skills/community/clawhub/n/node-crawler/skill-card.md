## Description: <br>
Node.js web crawler guidance for production-grade, large-scale scraping, batch downloads, multi-page crawling, long-running spiders, and complex workflows with rate limiting, retries, proxy rotation, and Cheerio parsing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike442144](https://clawhub.ai/user/mike442144) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design Node.js crawler workflows for bulk scraping, batch file downloads, paginated extraction, proxy-aware crawling, and resilient queue-based web spiders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Large-scale crawling can overload or violate rules for sites that have not authorized scraping. <br>
Mitigation: Confirm permission and applicable terms before crawling, keep rate limits conservative, and scope crawls to intended targets. <br>
Risk: Installed crawler dependencies may introduce supply-chain or runtime risk. <br>
Mitigation: Review the npm package and dependency versions before use, and install only from trusted registries. <br>
Risk: Examples that disable TLS verification or write downloaded files can be unsafe if copied into production unchanged. <br>
Mitigation: Keep TLS verification enabled except for controlled local debugging, and validate download paths and filenames before writing files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mike442144/node-crawler) <br>
- [Options Reference](references/options.md) <br>
- [Code Examples](references/examples.md) <br>
- [Got Options Documentation](https://github.com/sindresorhus/got/blob/main/documentation/2-options.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JavaScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing examples and option guidance for Node.js crawler usage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
