## Description:

Supports deterministic causal decision analysis, scenario stress testing, and auditable decision reports with the NOMOS engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nohn3043-arch](https://clawhub.ai/user/nohn3043-arch)

### License/Terms of Use:

Software License Agreement v1.2 (commercial use requires written authorization)

## Use Case:

Developers and decision reviewers use the engine to assess declared alternatives, test assumptions and scenarios, trace causal reasoning, and inspect auditable reports. Commercial use requires written authorization; avoid shared enterprise API deployments until tenant enforcement and identity handling are fixed.

### Deployment Geography for Use:

Global, subject to the bundled license's regional authorization terms

## Known Risks and Mitigations:

Risk: The enterprise API claims tenant isolation but can store and retrieve key records globally, risking cross-tenant access in shared deployments.

Mitigation: Use only isolated research, local demos, or carefully single-tenant deployments until tenant-scoped storage and queries, claim-derived tenant resolution, and cross-tenant access tests are in place; do not expose the shared enterprise API.

Risk: The identity endpoint needs correction before the enterprise API can be relied on for tenant isolation.

Mitigation: Fix and test the identity endpoint and strict claim-derived tenant resolution before any shared deployment.

## Reference(s):

- [ClawHub release](https://clawhub.ai/nohn3043-arch/skills/nomos-decision-hub)
- [Publisher-listed project homepage (not verified import provenance)](https://github.com/nohn3043-arch/NOMOS)
- [Sealed Report specification](references/SealedReportSpec.md)
- [Decision Scenario Library](references/DecisionScenarioLibrary.md)
- [Third-Party Verification Guide](docs/VERIFICATION_GUIDE.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON reports, Code, Shell commands, Configuration guidance]

**Output Format:** [Text and Markdown guidance; structured JSON decision and audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include causal traces, scenario results, and verifiable audit hashes; final decisions remain with people.]

## Skill Version(s):

2.1.0 (source: ClawHub release and SKILL.md frontmatter; bundled engine 0.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
