## Description: <br>
Fast lightweight translation for short texts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to translate short text through the NEXUS hosted service using payment-backed API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Translated text and payment proof or payment credentials are sent to the NEXUS hosted service. <br>
Mitigation: Use only for text approved for external processing, and avoid secrets, regulated data, or confidential business text unless external processing is approved. <br>
Risk: The skill can make paid translation requests. <br>
Mitigation: Use sandbox or scoped payment credentials and configure the agent to ask before making paid translation requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/nexus-quick-translate) <br>
- [Publisher Profile](https://clawhub.ai/user/cyberforexblockchain) <br>
- [NEXUS Platform](https://ai-service-hub-15.emergent.host) <br>
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>
- [A2A Agent Card](https://ai-service-hub-15.emergent.host/.well-known/agent.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [JSON object with a result string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote HTTPS service response; paid requests require payment proof or payment credentials.] <br>

## Skill Version(s): <br>
2.1.0 (source: ClawHub release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
