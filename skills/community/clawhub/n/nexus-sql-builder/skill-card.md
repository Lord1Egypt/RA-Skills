## Description: <br>
Generate complex SQL queries from requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn natural-language SQL requirements into generated SQL through the NEXUS remote service. It is suited for workflows that can send SQL requirements, schema context, prompts, and payment credentials to a third-party API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send SQL requirements, schema details, prompts, and payment proofs to a third-party paid service. <br>
Mitigation: Install only if the publisher and NEXUS service are trusted, avoid secrets or regulated data in prompts, and use sandbox or narrowly scoped payment credentials where possible. <br>
Risk: The security scan summary says paid remote calls do not have well-defined consent boundaries. <br>
Mitigation: Configure the agent to require explicit approval before paid remote calls and review payment details before retrying with payment credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/nexus-sql-builder) <br>
- [Publisher profile](https://clawhub.ai/user/cyberforexblockchain) <br>
- [NEXUS platform](https://ai-service-hub-15.emergent.host) <br>
- [SQL builder API endpoint](https://ai-service-hub-15.emergent.host/api/original-services/sql-builder) <br>
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>
- [Stellar information](https://ai-service-hub-15.emergent.host/api/mpp/stellar) <br>
- [A2A agent card](https://ai-service-hub-15.emergent.host/.well-known/agent.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, API calls, guidance] <br>
**Output Format:** [JSON object with a result string, commonly containing generated SQL or SQL-building guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a remote HTTPS request and either an x402/MPP credential or NEXUS_PAYMENT_PROOF; sandbox_test is documented for testing.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
