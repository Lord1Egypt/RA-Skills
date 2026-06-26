## Description: <br>
LinkdAPI helps agents look up LinkedIn profiles, companies, jobs, posts, articles, and related B2B data through the LinkdAPI REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ethcipher](https://clawhub.ai/user/ethcipher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to perform LinkedIn data workflows such as lead enrichment, company research, people and job search, market intelligence, and content research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys could be exposed in chats, shell history, or logs. <br>
Mitigation: Use a dedicated LinkdAPI key, keep it in the LINKDAPI_KEY environment variable, and avoid pasting or logging the key. <br>
Risk: LinkedIn profile, contact, and company data can include personal or sensitive business information. <br>
Mitigation: Handle retrieved data according to applicable privacy, consent, retention, and platform rules. <br>
Risk: High-volume lookups can consume LinkdAPI API credits quickly. <br>
Mitigation: Monitor API-credit usage and scope requests to the minimum data needed. <br>


## Reference(s): <br>
- [LinkdAPI API Reference](references/api-ref.md) <br>
- [LinkdAPI Endpoint Manifest](references/skills.json) <br>
- [LinkdAPI API Specification](https://linkdapi.com/apispec.yml) <br>
- [ClawHub Skill Page](https://clawhub.ai/ethcipher/linkdapi-official) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with REST API examples, endpoint references, and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the LINKDAPI_KEY environment variable and the X-linkdapi-apikey header; API responses use the LinkdAPI response envelope.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
