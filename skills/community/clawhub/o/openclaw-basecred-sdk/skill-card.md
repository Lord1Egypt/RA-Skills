## Description: <br>
Check human reputation via Ethos Network, Talent Protocol, and Farcaster using the neutral basecred-sdk to fetch raw scores, levels, and signals for identity verification and trust assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teeclaw](https://clawhub.ai/user/teeclaw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to query reputation signals for Ethereum addresses across Ethos Network, Talent Protocol, and Farcaster. It returns source-specific data for verification and trust assessment without making a trustworthiness decision for the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried wallet addresses may be sent to Ethos, Talent Protocol, and Neynar/Farcaster depending on available providers and credentials. <br>
Mitigation: Use the skill only when those provider lookups are acceptable for the address being checked, and avoid submitting addresses that should not be shared with these services. <br>
Risk: Optional Talent Protocol and Neynar API keys are read from the user's OpenClaw environment file. <br>
Mitigation: Store provider keys only in the expected credential location, keep file permissions restricted, and rotate keys if exposure is suspected. <br>
Risk: Dependency updates could change provider behavior or credential handling. <br>
Mitigation: Use the lockfile or verify dependency versions before upgrading, and re-review the security posture after dependency changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/teeclaw/openclaw-basecred-sdk) <br>
- [basecred SDK npm Package](https://www.npmjs.com/package/@basecred/sdk) <br>
- [basecred SDK Output Schema](https://github.com/Callmedas69/basecred/tree/main/packages/sdk#output-schema) <br>
- [Ethos Network](https://ethos.network) <br>
- [Talent Protocol](https://talentprotocol.com) <br>
- [Neynar](https://neynar.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON summary or full profile, with optional human-readable text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; optional TALENT_API_KEY and NEYNAR_API_KEY enable additional provider data.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence, package.json, CHANGELOG released 2026-02-11) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
