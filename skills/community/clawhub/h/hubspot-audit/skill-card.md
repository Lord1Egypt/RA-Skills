## Description: <br>
Run a comprehensive HubSpot CRM database audit that analyzes contacts, companies, deals, engagement, data quality, and deliverability for CRM cleanup, client onboarding, or quarterly health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomgranot](https://clawhub.ai/user/tomgranot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
CRM administrators, RevOps teams, and consultants use this skill to audit a HubSpot portal across data quality, deliverability, engagement, ownership, automation, and pipeline health. The skill helps produce a graded markdown report and an ordered cleanup prescription. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HubSpot CRM records and private app tokens are sensitive and could be exposed through local files or generated reports. <br>
Mitigation: Use a dedicated least-privilege HubSpot token, keep .env and reports out of source control, and treat generated reports as confidential. <br>
Risk: The artifact includes optional repository-changing behavior for creating skills, pushing branches, forking, and opening pull requests. <br>
Mitigation: Do not allow the skill to create skills, commit, push, fork, or open pull requests unless the user explicitly requests that separate workflow. <br>
Risk: Large HubSpot portals can produce incomplete or misleading counts if API limits, null checks, pagination, and rate limits are mishandled. <br>
Mitigation: Use the documented HubSpot null-check operators, segment Search API queries that may exceed 10,000 results, and apply delays or exponential backoff for rate limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tomgranot/hubspot-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with Python code, shell commands, configuration notes, and ordered recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reports/hubspot-audit-{YYYY-MM-DD}.md and may guide creation of scripts/audit_portal.py when run by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
