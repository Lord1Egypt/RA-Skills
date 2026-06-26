## Description: <br>
Convert meeting transcripts into structured notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to send meeting transcript text to the NEXUS service and receive structured meeting notes. It is intended for workflows where a paid remote notes service and payment proof handling are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting transcript content is sent to the NEXUS remote service for processing. <br>
Mitigation: Avoid sending confidential, regulated, HR, legal, or client-sensitive meeting content unless third-party processing is approved. <br>
Risk: The skill supports paid workflows and broad payment proof handling. <br>
Mitigation: Use the sandbox mode before paid use, verify payment requirements before authorizing payment, and install only if NEXUS is trusted to process payment proofs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyberforexblockchain/nexus-meeting-notes) <br>
- [NEXUS Agent-as-a-Service platform](https://ai-service-hub-15.emergent.host) <br>
- [Meeting notes API endpoint](https://ai-service-hub-15.emergent.host/api/original-services/meeting-notes) <br>
- [MPP discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [x402 discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [Stablecoin registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured service response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns meeting-note content from a remote NEXUS API after payment proof or sandbox authorization.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
