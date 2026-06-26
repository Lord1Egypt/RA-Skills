## Description: <br>
Event tracking, funnel analysis, cohort retention, multi-touch attribution, revenue metrics, and real-time analytics - built for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cameron48](https://clawhub.ai/user/cameron48) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to connect AI agents to paid analytics endpoints for tracking events, analyzing funnels and cohorts, monitoring attribution, and retrieving revenue metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Analytics requests may send sensitive prompts, regulated data, secrets, or direct personal identifiers to an external paid service. <br>
Mitigation: Avoid sending secrets, raw prompts, regulated data, or direct personal identifiers unless a policy, consent basis, and data handling review are in place. <br>
Risk: Each endpoint uses x402 payment, so frequent analytics calls can accumulate USDC costs. <br>
Mitigation: Monitor x402 payment usage and set agent-side limits or approval gates for high-frequency calls. <br>


## Reference(s): <br>
- [Analytics Engine Gateway](https://gateway.mcfagentic.com) <br>
- [ClawHub listing](https://clawhub.ai/cameron48/mcf-analytics-engine) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documents x402-paid analytics endpoints and request paths for agent integration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
