## Description: <br>
Generate changelogs from git commits or descriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release maintainers use this skill to turn commit history, release notes, or descriptive change text into a changelog through the NEXUS remote service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic invocation can spend funds through a paid remote changelog service. <br>
Mitigation: Configure the agent to ask before paid calls, start with sandbox or low-value credentials, and review payment prompts before retrying requests. <br>
Risk: Changelog source text and payment proof data are sent to a third-party remote service. <br>
Mitigation: Avoid sending secrets, private unreleased repository data, or high-value payment credentials unless the NEXUS service is trusted for that data. <br>
Risk: Security evidence marks the release suspicious because paid remote execution combines spending and privacy risk. <br>
Mitigation: Install only after reviewing the disclosed service behavior, required environment variable, and organization policy for paid external API calls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/nexus-changelog) <br>
- [NEXUS Platform](https://ai-service-hub-15.emergent.host) <br>
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>
- [A2A Agent Card](https://ai-service-hub-15.emergent.host/.well-known/agent.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [JSON service response containing generated changelog text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a payment credential or sandbox proof through NEXUS_PAYMENT_PROOF, X-PAYMENT, or Authorization: Payment.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
