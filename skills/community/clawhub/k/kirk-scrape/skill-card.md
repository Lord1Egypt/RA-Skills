## Description: <br>
Provides legal web scraping guidance and code patterns for robots.txt checks, rate limiting, GDPR/CCPA-aware data handling, direct HTTP scraping, and managed scraping through SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to plan and implement compliant public web scraping workflows, including pre-scrape legal checks, request throttling, data minimization, and optional managed extraction through SkillBoss API Hub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API examples require a SkillBoss API key and reference inconsistent provider domains. <br>
Mitigation: Confirm the correct provider domain before use and prefer a scoped or test API key. <br>
Risk: Managed scraping and chained LLM analysis may send scraped page content to an external service. <br>
Mitigation: Use only permitted public pages and avoid sending personal, confidential, copyrighted, login-protected, or restricted content. <br>
Risk: Scraping can violate site terms, robots.txt rules, privacy law, or copyright obligations. <br>
Mitigation: Run the pre-scrape checklist, honor robots.txt and rate limits, prefer official APIs, and minimize stored data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/kirk-scrape) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [Code patterns](artifact/code.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include examples that require SKILLBOSS_API_KEY for managed scraping and external LLM analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
