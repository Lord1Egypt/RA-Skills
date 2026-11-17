## Description:

Diagnose slow PikPak downloads with a controlled A/B speed test, then pick between client, WebDAV and third-party tools on evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipiguai87-alt](https://clawhub.ai/user/pipiguai87-alt)

### License/Terms of Use:

MIT-0

## Use Case:

People troubleshooting slow PikPak downloads or playback use this skill to compare authorized file samples and choose a client or access path based on measured evidence. It explains limits and costs so a small test is not mistaken for guaranteed sustained speed or a way around account quotas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Signed download links can contain access credentials, and test traffic may incur data or account quota costs.

Mitigation: Keep authorized links in private local files, never paste them into chat or screenshots, and check traffic costs before running a test.

Risk: The diagnostics bypass configured proxies, while short file-prefix samples may not represent sustained downloads or playback behavior.

Mitigation: Label results as direct_no_proxy, compare the same authorized file under controlled conditions, and verify sustained speed and playback separately.

## Reference(s):

- [PikPak: Why download speed may be slow](https://mypikpak.com/zh-CN/help-center/play_and_download/download_speed/why)
- [PikPak WebDAV setup and permissions](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/how_to)
- [PikPak connected-app quota](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/speed_limit)
- [rclone PikPak backend](https://rclone.org/pikpak/)
- [Upstream design and risk review](artifact/references/upstream-design.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands, Guidance]

**Output Format:** [JSON diagnostic reports and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports observations, bounded sample measurements, and evidence-based recommendations; does not promise sustained speed improvement.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
