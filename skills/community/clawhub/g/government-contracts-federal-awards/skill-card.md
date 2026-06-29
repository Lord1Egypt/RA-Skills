## Description: <br>
Government Contracts & Federal Awards helps agents look up U.S. federal contract awards by company or keyword, identify recent winners, and surface GovCon sales-intent signals through paid HTTPS endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colinhughes2121](https://clawhub.ai/user/colinhughes2121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents, analysts, and sales teams use this skill to research U.S. government contractors, find procurement opportunities by topic, and identify recent federal award winners for lead qualification or competitor tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-initiated paid x402 API lookups can incur repeated USDC charges. <br>
Mitigation: Use wallet or spending controls and review lookup frequency before enabling frequent or automated searches. <br>
Risk: Company names or search keywords are sent to GoCreative when the endpoints are called. <br>
Mitigation: Avoid submitting sensitive internal terms unless that data sharing is approved for the user's environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/colinhughes2121/government-contracts-federal-awards) <br>
- [GoCreative API](https://api.gocreativeai.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Guidance] <br>
**Output Format:** [JSON responses from HTTPS GET endpoints, typically summarized by the agent in text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid x402 requests may send company names or search keywords to GoCreative and incur per-call USDC charges.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
