## Description: <br>
Convert natural language to optimized SQL queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to turn natural-language database questions into optimized SQL query text through the hosted NEXUS service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, schema details, and payment proof credentials may be sent to a third-party hosted service. <br>
Mitigation: Use sandbox_test first, avoid secrets or private database data in prompts, and install only if you trust NEXUS. <br>
Risk: Automatic invocation could submit paid requests or spend payment credentials without clear per-call controls. <br>
Mitigation: Configure agent-level confirmation, budget, and spending limits before enabling automatic invocation. <br>
Risk: Generated SQL can be incorrect or unsafe for a target database. <br>
Mitigation: Review generated queries before execution and test against non-production data before using them on live systems. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/cyberforexblockchain/nexus-text-to-sql) <br>
- [NEXUS platform](https://ai-service-hub-15.emergent.host) <br>
- [Text-to-SQL API endpoint](https://ai-service-hub-15.emergent.host/api/original-services/text-to-sql) <br>
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [JSON object with a result string containing SQL-oriented text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NEXUS_PAYMENT_PROOF or a supported payment credential; sandbox_test is documented for testing.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
