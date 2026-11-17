## Description:

This Chinese-language skill helps agents evaluate a cautious content-layer partial migration from Nolan AI to AI-HIVE MCP, including capability checks, sample-shot planning, approvals, cost and quality metrics, and rollback boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and developers use this skill to assess whether selected Nolan AI image, video, or shot nodes can be partially migrated to AI-HIVE while preserving human approval, rollback, and measurable quality and cost checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to contact AI-HIVE or Nolan AI-related web resources.

Mitigation: Confirm the current platform capabilities and terms before relying on them, and keep the migration limited to independently verifiable content nodes.

Risk: Media generation can create cost exposure or publish unreviewed outputs.

Mitigation: Require budget and human approval before paid generation, external sharing, or publication, and stop migration when cost, quality, or rollback checks fail.

Risk: Uploaded references can include unauthorized people, brands, IP, music, or video assets.

Mitigation: Use only owned or authorized assets, retain source and file-hash records, and stop work when rights are unclear.

Risk: Migration claims could overstate equivalence with Nolan AI.

Mitigation: Use same-day, same-input comparison samples before making comparative claims, and avoid claims of full replacement, official partnership, lowest price, or superior performance without direct evidence.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/nolan-ai-film-agent-ai-hive-migration)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [Nolan AI official source](https://trynolan.io/)
- [Platform evidence and migration boundaries](references/platform-evidence.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON task-contract examples and shell or tool-listing commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve approval gates, authorized-asset requirements, cost snapshots, quality metrics, and rollback criteria.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
