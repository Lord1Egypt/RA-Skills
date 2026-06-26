## Description: <br>
Use this skill when the user asks for a quote, estimate, price, or "how much" for a UK trades job - electrical, plumbing, locksmith, glazing, carpentry, handyperson, heating, gas, roofing, drains, white goods, or boiler service. Calls the JustFix Estimator MCP server to return a cost breakdown, scope summary, and a tappable booking link that completes the booking in the browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adam-graham](https://clawhub.ai/user/adam-graham) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users in the UK use this skill to get home-services labour estimates and booking links from an AI agent. Developers can add JustFix quote generation to agent workflows without requiring API keys or customer credentials. <br>

### Deployment Geography for Use: <br>
United Kingdom <br>

## Known Risks and Mitigations: <br>
Risk: User job descriptions are sent to JustFix's public MCP service. <br>
Mitigation: Use the skill only for UK trades quote requests and avoid sending unnecessary personal or sensitive details. <br>
Risk: Booking links lead users to JustFix and include a unique attribution ID. <br>
Mitigation: Disclose that the link opens JustFix before the user clicks, and pass the returned booking URL through unchanged. <br>
Risk: Broad activation guidance can cause the skill to trigger on loosely related home-services conversations. <br>
Mitigation: Configure narrow triggers and confirm UK quote or booking intent before calling the estimator. <br>
Risk: The estimate does not include live availability, payment collection, or parts and materials. <br>
Mitigation: State the labour-only scope, estimated duration, call-out fee, and final-invoice caveat in the agent response. <br>


## Reference(s): <br>
- [JustFix skill repository](https://github.com/Just-Fix/justfix-skill) <br>
- [JustFix homepage](https://justfix.app) <br>
- [JustFix Estimator MCP endpoint](https://estimator-mcp.justfix.app/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/adam-graham/justfix) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown or plain text quote card with cost breakdown and booking URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a unique JustFix booking URL with attribution ID; estimates are labour-only and final invoice can vary with actual time spent.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
