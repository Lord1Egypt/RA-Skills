## Description: <br>
Audits HTTP security response headers for a URL or local dev server, grades missing or weak protections, and proposes configuration fixes for common web servers and frameworks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and DevOps teams use this skill to inspect response headers on sites or local services and receive prioritized remediation guidance. It can generate nginx, Apache, Next.js, or similar configuration snippets for missing or weak headers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes network requests to user-provided URLs, including possible localhost or private-network targets. <br>
Mitigation: Run it only against systems you own or have permission to test, and review localhost, private-network, cloud metadata, and redirect targets before execution. <br>
Risk: Generated header fixes can affect site behavior if applied without adaptation. <br>
Mitigation: Review configuration snippets in a staging environment and adjust CSP, HSTS, and cross-origin policies for the application's actual dependencies before deploying. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-security-headers) <br>
- [Canlah AI homepage](https://canlah.ai) <br>
- [HSTS preload list](https://hstspreload.org) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with grades, command examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated nginx, Apache, Next.js, or Cloudflare Workers header recommendations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and frontmatter metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
