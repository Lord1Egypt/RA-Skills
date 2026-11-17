## Description:

Automatically gathers Nintendo-related public sources to produce a Chinese daily Nintendo Switch report covering recent game news, upcoming eShop releases, and system updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benzking](https://clawhub.ai/user/benzking)

### License/Terms of Use:

MIT-0

## Use Case:

External users, gaming-news editors, and community managers use this skill to create a concise Chinese Nintendo Switch daily report with linked source references. It focuses on recent game news, releases in the next seven days, and recent system-update announcements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public web sources may be unavailable or stale, causing gaps in a daily report.

Mitigation: State unavailable sources in the report and prefer accessible Nintendo Hong Kong and Taiwan sources when alternates fail.

Risk: The system-update section may be inconsistent when there is no recent update.

Mitigation: Use an explicit no-update statement when no system update is found in the 36-hour window.

## Reference(s):

- [Nintendo Hong Kong Topics](https://www.nintendo.com.hk/hk/topics/)
- [Nintendo Hong Kong Release Schedule](https://www.nintendo.com.hk/hk/schedule/)
- [Nintendo Hong Kong eShop Titles](https://ec.nintendo.com/HK/zh/titles/)
- [Nintendo Taiwan Topics](https://www.nintendo.com.tw/topics/)
- [Nintendo Taiwan Switch Software](https://www.nintendo.com.tw/tw/software/switch/)
- [Nintendo Japan](https://www.nintendo.co.jp/)
- [Bahamut GNN](https://gnn.gamer.com.tw/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese Markdown report with source links and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers the previous 36 hours for news and the next seven days for upcoming releases.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
