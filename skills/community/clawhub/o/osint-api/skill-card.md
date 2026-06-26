## Description: <br>
AI-powered OSINT intelligence reports via API, with multiple RSS feeds across 15 categories, enriched analysis, domain reconnaissance, social lookup, and breach checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahsan3274](https://clawhub.ai/user/ahsan3274) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, OSINT analysts, and developers use this skill to let an agent request intelligence briefings, domain reconnaissance, social profile lookup, and breach checks from the hosted OSINT API. It is useful when an agent needs structured OSINT results without maintaining its own feed collection or enrichment pipeline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lookup targets, including domains, usernames, and email addresses for breach checks, are sent to the hosted OSINT API along with the OSINT_API_KEY. <br>
Mitigation: Use the skill only for authorized investigations and avoid submitting sensitive client, employee, or third-party identifiers unless the provider's privacy, retention, and billing terms have been reviewed. <br>
Risk: The skill depends on a third-party hosted API for availability, retention behavior, pricing, and response quality. <br>
Mitigation: Confirm the API provider's terms before production use, monitor returned results for accuracy, and treat API failures or stale cached responses as normal operational conditions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ahsan3274/osint-api) <br>
- [OSINT API endpoint](https://osint.ahsan-tariq-ai.xyz/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON API responses and CLI text, with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OSINT_API_KEY and sends authenticated HTTPS requests to osint.ahsan-tariq-ai.xyz for reports, categories, domain reconnaissance, social lookup, and breach checks.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
