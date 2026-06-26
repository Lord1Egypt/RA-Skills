## Description: <br>
Maxhub Linkedin helps agents query and analyze LinkedIn professional data, including people, companies, jobs, posts, comments, ads, and related business intelligence, through the MaxHub API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiewxx](https://clawhub.ai/user/xiewxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill for authorized B2B research, recruiting analysis, company intelligence, job discovery, and LinkedIn content analysis using MaxHub API data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LinkedIn identifiers, search terms, URLs, and possible profile or contact data are transmitted to a third-party MaxHub API. <br>
Mitigation: Use only for authorized business or recruiting research, minimize personal data, and avoid bulk people or contact harvesting. <br>
Risk: The skill may expose sensitive API keys, cookies, or session tokens if they are pasted into prompts, logs, or shared outputs. <br>
Mitigation: Use the MAXHUB_API_KEY environment variable, avoid production cookies or session tokens, rotate credentials, and do not include secrets in logs or user-visible responses. <br>
Risk: Broad read-only endpoint routing can still support person profiling or contact-information lookups without strong consent gates. <br>
Mitigation: Require explicit user confirmation before contact-info or person-profiling lookups and follow the documented endpoint whitelist and recipe flow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiewxx/maxhub-linkedin) <br>
- [MaxHub Website](https://www.aconfig.cn) <br>
- [README](README.md) <br>
- [User and People Reference](references/user.md) <br>
- [Company Reference](references/company.md) <br>
- [Jobs Reference](references/jobs.md) <br>
- [Content and Ads Reference](references/content.md) <br>
- [Recipe Index](references/recipes/_index.md) <br>
- [Parameter and Field Mapping Index](references/param-mappings.md) <br>
- [Endpoint Whitelist](references/endpoints_whitelist.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Guidance, Analysis, Markdown] <br>
**Output Format:** [Markdown guidance with curl commands and JSON-derived API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAXHUB_API_KEY and sends authorized LinkedIn identifiers, keywords, URLs, and optional cookies or tokens to https://www.aconfig.cn.] <br>

## Skill Version(s): <br>
3.8.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
