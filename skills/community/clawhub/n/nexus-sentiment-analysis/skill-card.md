## Description: <br>
Analyze emotional tone and detect opinions through the NEXUS remote sentiment-analysis service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send text to the NEXUS API for sentiment and opinion analysis. It is suited to workflows that can approve remote processing and paid per-request access before submitting content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends submitted text to a third-party NEXUS service for remote analysis. <br>
Mitigation: Do not submit secrets, regulated data, or confidential business content unless third-party processing has been approved. <br>
Risk: Normal use may incur per-request payment through supported payment protocols. <br>
Mitigation: Use the documented sandbox payment proof for testing and confirm payment requirements before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/nexus-sentiment-analysis) <br>
- [NEXUS platform](https://ai-service-hub-15.emergent.host) <br>
- [Sentiment analysis API endpoint](https://ai-service-hub-15.emergent.host/api/original-services/sentiment-analysis) <br>
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [AP2 configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API responses and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NEXUS_PAYMENT_PROOF for paid access; sandbox_test is documented for testing.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
