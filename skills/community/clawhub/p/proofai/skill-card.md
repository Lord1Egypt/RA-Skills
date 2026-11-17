## Description:

Provides cryptographic proof workflows for AI decisions, including certification, logging, verification, and monitoring for compliance use cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scorentab-afk](https://clawhub.ai/user/scorentab-afk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and compliance teams use this skill to certify, log, verify, and monitor AI decisions with tamper-evident evidence bundles and blockchain verification links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and responses may be sent to external ProofAI/Supabase-backed services.

Mitigation: Use only data that the organization has approved for submission to those services, and do not submit secrets, regulated personal data, confidential source code, contracts, or customer data without approval.

Risk: Evidence bundles may create durable proof records, including blockchain anchoring.

Mitigation: Confirm user consent, retention expectations, and the blockchain anchoring model before certifying or logging AI decisions.

Risk: Unpinned package execution or an untrusted PROOFAI_API_URL can redirect sensitive decision data.

Mitigation: Pin the npm package version, avoid unreviewed npx -y execution, and keep PROOFAI_API_URL limited to trusted endpoints.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/scorentab-afk/skills/proofai)
- [ProofAI npm SDK](https://www.npmjs.com/package/@proofai/sdk)
- [ProofAI Regulator Portal](https://proofai-ochre.vercel.app/regulator)

## Skill Output:

**Output Type(s):** [text, JSON, verification links]

**Output Format:** [Plain text and JSON returned through MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bundle IDs, bundle hashes, verification status, Polygon transaction data, monitoring statistics, truncated AI response previews, and error messages.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
