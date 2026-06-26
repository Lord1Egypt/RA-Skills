## Description: <br>
HTTP Cache Audit analyzes HTTP caching headers for URLs and local development servers, then reports cache policy issues and suggests fixes for browsers, CDNs, and common web server configurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and web performance engineers use this skill to audit Cache-Control, validation, Vary, CDN cache status, and stale-while-revalidate behavior for web assets and APIs. It helps identify misconfigured cache policies and generate practical nginx, Apache, Cloudflare, Fastly, or Next.js configuration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security adjudication noted low confidence because scanner context lacked local artifact contents. <br>
Mitigation: Review the skill files and install steps before deployment; the supplied scanner signals did not identify a security concern. <br>
Risk: The skill audits URLs by issuing HTTP header requests, so it may contact external or internal services selected by the user. <br>
Mitigation: Use it only against systems the operator is authorized to test and review generated cache changes before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-http-cache-audit) <br>
- [PHY041 publisher profile](https://clawhub.ai/user/PHY041) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cache grades, issue summaries, curl verification commands, and nginx, Apache, Cloudflare, Fastly, or Next.js cache configuration examples.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
