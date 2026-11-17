## Description:

Analyze emotional tone and detect opinions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to send text to the NEXUS service for sentiment and opinion analysis in agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for analysis and payment proof data are sent to the remote NEXUS service.

Mitigation: Do not submit secrets, regulated data, or proprietary text unless NEXUS is approved for the use case.

Risk: The skill advertises paid per-request API usage.

Mitigation: Monitor usage and payment proof configuration before enabling the skill in automated workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/skills/nexus-sentiment-analysis)
- [NEXUS Platform](https://ai-service-hub-15.emergent.host)
- [Sentiment Analysis API Endpoint](https://ai-service-hub-15.emergent.host/api/original-services/sentiment-analysis)
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402)
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover)
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON object containing a service response string.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The response is produced by a paid remote NEXUS API call.]

## Skill Version(s):

2.1.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
