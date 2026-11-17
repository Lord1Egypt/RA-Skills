## Description:

Use when using Feishu/Lark Sheets through lark-cli or feishu-cli for office reports, QA matrices, release checklists, KPI trackers, imports/exports, tabular analysis, and Dev Hub artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afengzi](https://clawhub.ai/user/afengzi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide agents working with Feishu/Lark Sheets for operational reporting, QA matrices, release checklists, KPI trackers, tabular analysis, imports, exports, and Dev Hub artifact snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sheet commands can read or change Lark/Feishu office data under the user's authorization.

Mitigation: Review sheet URLs, ranges, and local JSON files before allowing read, append, dropdown, or export commands.

Risk: Exported Sheet snapshots and Dev Hub artifact records may contain sensitive operational data.

Mitigation: Review exported files and artifact summaries before retaining or sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/afengzi/skills/lark-cli-devhub-sheets)
- [ClawHub publisher profile](https://clawhub.ai/user/afengzi)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-authorized lark-cli or feishu-cli environment.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
