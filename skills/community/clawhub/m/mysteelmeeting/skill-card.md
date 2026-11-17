## Description:

Searches Mysteel conference listings by industry, region or province, status, fee type, activity type, keyword, and pagination options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wyb92](https://clawhub.ai/user/wyb92)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find Mysteel industry conferences and inspect meeting status, location, dates, fees, and detail links. It is useful for filtering Chinese-language conference information across steel, coal, non-ferrous metals, new energy, agriculture, and related industries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and filters may be sent to huizhan.mysteel.com when live queries or category refreshes run.

Mitigation: Avoid entering confidential search terms or sensitive business planning details unless this network use is acceptable.

Risk: Temporary industry and area category cache files are stored inside the skill directory.

Mitigation: Use the documented cache-clearing option or remove cache files before packaging or sharing when cached category data should not persist.

## Reference(s):

- [我的钢铁网会议查询 API 参考](references/api_reference.md)
- [Mysteel conference activity API](https://huizhan.mysteel.com/event/activity)
- [ClawHub skill page](https://clawhub.ai/wyb92/skills/mysteelmeeting)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text query results with command-line examples and returned conference details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include meeting status, location, dates, fee information, total counts, pagination, and detail URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
