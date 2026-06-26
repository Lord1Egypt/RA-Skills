## Description: <br>
Generate and explain regular expressions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to request regular-expression generation and explanations from the hosted NEXUS service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User prompts, examples, logs, snippets, and payment credentials may be sent to an external paid API. <br>
Mitigation: Install only if you trust NEXUS, avoid submitting secrets or regulated data, and use sandbox or narrowly scoped payment credentials. <br>
Risk: The service can make paid network calls without clearly defined per-use controls. <br>
Mitigation: Configure the agent to ask before network or paid calls and review payment requirements before authorizing requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/nexus-regex-generator) <br>
- [NEXUS platform](https://ai-service-hub-15.emergent.host) <br>
- [Regex Generator API endpoint](https://ai-service-hub-15.emergent.host/api/original-services/regex-generator) <br>
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Guidance] <br>
**Output Format:** [JSON object with a result string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated regular expressions and explanatory text returned by the hosted service.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
