## Description: <br>
Nex Domains helps agents manage a local domain portfolio by tracking registrars, DNS records, WHOIS data, SSL certificate expiry, health checks, costs, client assignments, and CSV or JSON exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexaiguy](https://clawhub.ai/user/nexaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Domain managers, DevOps teams, web agencies, and system administrators use this skill to inventory domains, monitor expiration and SSL status, inspect DNS and WHOIS details, sync Cloudflare zones, and export portfolio data for reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Cloudflare and registrar credentials and stores domain, DNS, client, cost, and portfolio details locally. <br>
Mitigation: Use least-privilege API tokens, protect registrar credentials and private keys, and restrict access to the local data directory and exported files. <br>
Risk: Removing a domain from tracking or exporting portfolio data can affect operational records or expose sensitive business details. <br>
Mitigation: Confirm intent before running removal commands and review export destinations before sharing or storing generated CSV or JSON files. <br>


## Reference(s): <br>
- [Nex AI homepage](https://nex-ai.be) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Plain text responses with optional CSV or JSON export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local storage and optional Cloudflare or TransIP credentials when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
