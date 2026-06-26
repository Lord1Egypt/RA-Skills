## Description: <br>
Legal web scraping with robots.txt compliance, rate limiting, and GDPR/CCPA-aware data handling. Supports both direct HTTP scraping and managed scraping via SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to plan and implement legally cautious web scraping workflows with robots.txt checks, request throttling, audit logging, and privacy-aware data handling. It also provides examples for managed scraping and optional LLM analysis through SkillBoss API Hub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Managed examples may send target URLs and scraped page content to SkillBoss API Hub. <br>
Mitigation: Use managed scraping only when the site and data handling requirements permit external processing, and avoid login-protected or personal data unless authorization is clear. <br>
Risk: Scraping can violate site terms, privacy requirements, or access controls if used without review. <br>
Mitigation: Check robots.txt, terms of service, available APIs, authentication boundaries, and data minimization requirements before collecting content. <br>
Risk: The robots.txt helper allows scraping when fetching robots.txt fails. <br>
Mitigation: Change the helper to fail closed or require explicit human approval before scraping after a robots.txt fetch error. <br>
Risk: The managed scraping flow requires a sensitive API key. <br>
Mitigation: Store SKILLBOSS_API_KEY in a protected secret manager or environment variable and avoid logging or committing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/jx-scrape) <br>
- [Code patterns](code.md) <br>
- [SkillBoss API Hub pilot endpoint](https://api.skillbossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with Python code examples and API request patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for managed scraping examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
