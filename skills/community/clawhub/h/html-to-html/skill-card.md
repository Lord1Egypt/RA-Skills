## Description: <br>
Clean and restructure messy or complex HTML documents using MinerU, producing clean, well-formatted HTML while preserving core content structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content migration teams, and web content maintainers use this skill to clean scraped pages, CMS exports, legacy HTML, or local HTML files into structured HTML through MinerU. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTML pages, URLs, or local exports may contain confidential, regulated, or proprietary information. <br>
Mitigation: Only process content with MinerU when its data handling is acceptable for the use case. <br>
Risk: The skill requires MINERU_TOKEN for HTML output. <br>
Mitigation: Treat MINERU_TOKEN as a secret and avoid exposing it in logs, shared shell history, or generated documents. <br>


## Reference(s): <br>
- [HTML to HTML ClawHub release](https://clawhub.ai/mzlzyca/html-to-html) <br>
- [MinerU homepage](https://mineru.net) <br>
- [MinerU token management](https://mineru.net/apiManage/token) <br>
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; the agent workflow produces clean structured HTML through MinerU CLI output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mineru-open-api and MINERU_TOKEN; document content is written to stdout by default or saved with -o.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
