## Description:

This skill helps HuahuaDaily users create versioned investment policies and generate auditable mutual-fund hold, add, reduce, rebalance, or cash-wait recommendations from live holdings, research evidence, and deterministic allocation logic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baiye1997](https://clawhub.ai/user/baiye1997)

### License/Terms of Use:

MIT-0

## Use Case:

External HuahuaDaily users and their agents use this skill to review personal mutual-fund holdings, maintain an investor policy, evaluate allocation changes, and produce a single auditable proposal for holding, adding, reducing, rebalancing, or waiting in cash. It is intended for user-confirmed advisory workflows and does not execute trades without user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes live-looking private portfolio snapshots in work/decision-input.json and work/decision-result.json.

Mitigation: Remove bundled work snapshots before publishing or installing broadly, and require fresh per-user data at runtime.

Risk: The skill reads live holdings and can retain local policy and activity history.

Mitigation: Install only for intended HuahuaDaily mutual-fund advisory use, document exact tool and storage permissions, and scope stored state per user.

Risk: Broad automatic invocation for financial advice could surface recommendations without deliberate user intent.

Mitigation: Disable or tightly constrain implicit invocation and require explicit user confirmation before policy changes or transaction requests.

## Reference(s):

- [Policy Contract](references/policy-contract.md)
- [Runtime and AI Research Protocol](references/runtime-protocol.md)
- [Decision and Allocation Core Contract](references/decision-contract.md)
- [Input Schema](references/input-schema.md)
- [Factor Model](references/factor-model.md)
- [Action Model](references/action-model.md)
- [AI Output Governance](references/ai-output-governance.json)
- [Report Contract](references/report-contract.md)
- [Controlled Evolution Protocol](references/evolution-protocol.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, HTML]

**Output Format:** [Chinese prose with structured decision summaries, JSON decision artifacts, shell commands, and optional self-contained HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory proposals; executable amounts and report fields are expected to come from deterministic artifacts and remain subject to user confirmation.]

## Skill Version(s):

4.3.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
