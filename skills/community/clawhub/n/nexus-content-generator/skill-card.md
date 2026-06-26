## Description: <br>
Create blog posts, social media, emails, marketing copy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate written content such as blog posts, social posts, email drafts, and marketing copy through the NEXUS remote AI service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid remote requests may be triggered without clear per-request control. <br>
Mitigation: Configure the agent to ask before sending content or spending payment proof on each request, and use sandbox mode before paid use. <br>
Risk: Prompts and content are sent to the NEXUS remote service. <br>
Mitigation: Install only if you trust NEXUS with the prompts you send, and avoid secrets or regulated data. <br>
Risk: The skill requires payment credentials or proof through NEXUS_PAYMENT_PROOF or payment headers. <br>
Mitigation: Limit payment proof exposure to this skill's intended runtime and review spending behavior before enabling automatic invocation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/nexus-content-generator) <br>
- [NEXUS Platform](https://ai-service-hub-15.emergent.host) <br>
- [Content Generator API](https://ai-service-hub-15.emergent.host/api/original-services/content-generator) <br>
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>
- [A2A Agent Card](https://ai-service-hub-15.emergent.host/.well-known/agent.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API response] <br>
**Output Format:** [JSON response containing generated content text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a paid remote API call or sandbox payment proof; content is returned by the NEXUS service.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
