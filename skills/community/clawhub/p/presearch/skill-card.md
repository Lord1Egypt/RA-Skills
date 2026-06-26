## Description: <br>
Production-ready decentralized search for AI agents via Presearch's privacy-first distributed node infrastructure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NosytLabs](https://clawhub.ai/user/NosytLabs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to query the Presearch Search API for web results in agent workflows that can issue authenticated HTTP GET requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may contain sensitive personal or business data sent to an external API. <br>
Mitigation: Avoid sensitive queries and use a dedicated Presearch API key where possible. <br>
Risk: Provider privacy or result-handling claims may not satisfy every compliance need. <br>
Mitigation: Independently verify Presearch privacy claims before using the skill for regulated or privacy-sensitive workflows. <br>
Risk: Bearer tokens can grant access to paid or rate-limited API usage if exposed. <br>
Mitigation: Keep API keys out of prompts, logs, and checked-in files; rotate keys if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/NosytLabs/presearch) <br>
- [Presearch Search API endpoint](https://na-us-1.presearch.com/v1/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP, JSON, Python, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Presearch Bearer token; API responses contain JSON search results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
