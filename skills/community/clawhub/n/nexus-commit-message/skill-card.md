## Description: <br>
Generate conventional commit messages from diffs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send repository diffs to the NEXUS service and receive conventional commit message text. It is suited for commit workflow assistance when the user accepts the remote processing and payment requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository diffs and payment proof data can be transmitted to a paid third-party API. <br>
Mitigation: Use sandbox mode first, redact secrets and proprietary content, and install only when the user trusts NEXUS to process the submitted data. <br>
Risk: Automatic invocation and payment boundaries are not clearly scoped. <br>
Mitigation: Require manual approval before any network call, wallet action, payment proof submission, or reusable payment mandate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/nexus-commit-message) <br>
- [NEXUS Platform](https://ai-service-hub-15.emergent.host) <br>
- [x402 Discovery](https://ai-service-hub-15.emergent.host/api/mpp/x402) <br>
- [MPP Discovery](https://ai-service-hub-15.emergent.host/api/mpp/discover) <br>
- [AP2 Configuration](https://ai-service-hub-15.emergent.host/api/ap2/config) <br>
- [XRPL Configuration](https://ai-service-hub-15.emergent.host/api/xrpl/config) <br>
- [Stablecoin Registry](https://ai-service-hub-15.emergent.host/api/mpp/stablecoins) <br>
- [A2A Agent Card](https://ai-service-hub-15.emergent.host/.well-known/agent.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [JSON service response with a generated commit message string, plus Markdown usage guidance and curl examples in the artifact documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NEXUS_PAYMENT_PROOF or supported x402, MPP, AP2, or legacy payment credentials before paid service calls.] <br>

## Skill Version(s): <br>
2.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
