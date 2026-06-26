## Description: <br>
ProofAI provides tools for certifying, logging, verifying, and monitoring AI decisions with cryptographic evidence for compliance workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scorentab-afk](https://clawhub.ai/user/scorentab-afk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and compliance teams use this skill to create tamper-evident records of AI prompts, responses, verification results, and post-market monitoring signals. It is intended for audit, regulator, client, and internal compliance review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Certified or logged AI prompts, responses, and metadata are sent to a third-party hosted service and may become long-lived audit evidence. <br>
Mitigation: Use only with organization-approved data, avoid secrets and regulated or sensitive material unless approved, and review retention, deletion, and blockchain anchoring implications before deployment. <br>
Risk: The skill requires API credentials for the hosted service. <br>
Mitigation: Protect and scope API keys, keep configuration files out of shared repositories, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub ProofAI listing](https://clawhub.ai/scorentab-afk/proofai) <br>
- [ProofAI GitHub repository](https://github.com/proof-ai/proofai) <br>
- [ProofAI npm SDK](https://www.npmjs.com/package/@proofai/sdk) <br>
- [ProofAI Regulator Portal](https://proofai-ochre.vercel.app/regulator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API calls, Guidance] <br>
**Output Format:** [Markdown text and JSON tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include evidence bundle identifiers, hashes, verification status, transaction hashes, Polygonscan URLs, monitoring statistics, and truncated AI responses.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
