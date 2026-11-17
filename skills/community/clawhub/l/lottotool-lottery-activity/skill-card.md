## Description:

Use when translating everyday lottery needs into LottoTool settings, planning or creating activities, finding activities, checking metrics, or exporting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zouzixuan](https://clawhub.ai/user/zouzixuan)

### License/Terms of Use:

MIT-0

## Use Case:

Event organizers and community or small-business operators use this skill to turn giveaway goals into lottery activity settings, plan and confirm new activities, check their own activity metrics, and export participant or winner data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating an activity can publish a live promotion with unintended settings.

Mitigation: Review the final preview and confirm the exact activity settings before creation.

Risk: OAuth authorization may grant access beyond what is needed for the requested task.

Mitigation: Review the requested OAuth permissions and authorize only when they match the intended activity operation.

Risk: Participant, winner, and form exports may contain personal information, and download links may expose it.

Mitigation: Share export files and their download links only with authorized recipients and protect them from unintended access.

Risk: Activity times can be misread if the displayed timezone is overlooked.

Mitigation: Interpret displayed times as Beijing time (UTC+8) and confirm the intended local time before publishing.

Risk: The remote service implementation has not been independently verified.

Mitigation: Check returned activity details and export results rather than assuming undocumented service behavior.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zouzixuan/skills/lottotool-lottery-activity)
- [Intent-to-settings guide](artifact/references/intent-to-settings.md)
- [Activity queries and data exports](artifact/references/activity-data.md)
- [Configuration schema guide](artifact/references/config-schema.md)
- [Connection and authorization guide](artifact/references/connection.md)
- [Usage examples](artifact/references/examples.md)
- [LottoTool MCP service](https://api.52choujiang.cn/lotto/mcp/v1)

## Skill Output:

**Output Type(s):** [Guidance, Text, Configuration, Files]

**Output Format:** [Conversational text or Markdown; exported data files in formats returned by the service, including CSV and XLSX]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include personal information in exported records; displayed times use Beijing time (UTC+8).]

## Skill Version(s):

1.2.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
