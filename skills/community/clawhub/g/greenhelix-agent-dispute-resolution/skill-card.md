## Description: <br>
Build automated dispute resolution pipelines, Verifiable Intent-compatible evidence chains, and chargeback defense workflows for agent-to-agent transactions involving escrow, SLA enforcement, and trust verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this guide to design agent-commerce dispute workflows, evidence packages, escrow controls, SLA monitoring, and chargeback defense patterns. The guidance is especially relevant for systems where autonomous agents initiate or respond to transactions that may affect funds or legal rights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide teaches autonomous escrow, dispute, refund, evidence-sharing, concession, and settlement workflows that can affect money or legal rights. <br>
Mitigation: Require human approval for escrow release or cancellation, dispute filing or response, concessions, settlements, and any irreversible money movement. <br>
Risk: Evidence bundles and dispute records may contain sensitive transaction, identity, authorization, or commercial information. <br>
Mitigation: Redact evidence bundles, use least-privilege API keys, force sandbox endpoints by default, add audit logs, and apply transaction caps before production use. <br>
Risk: Automated dispute and chargeback guidance may be misapplied without legal or compliance review. <br>
Mitigation: Route production policies through legal and compliance review, and monitor decisions with tamper-evident logs and post-dispute review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mirni/greenhelix-agent-dispute-resolution) <br>
- [GreenHelix Sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API](https://api.greenhelix.net/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guide with Python code examples and API call patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guide; examples should be adapted with sandbox endpoints, approval gates, redaction, caps, logging, and compliance review.] <br>

## Skill Version(s): <br>
1.3.1 (source: evidence release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
