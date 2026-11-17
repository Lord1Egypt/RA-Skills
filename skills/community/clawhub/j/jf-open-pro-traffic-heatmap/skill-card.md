## Description:

Analyzes indoor foot traffic from JF camera captures with local YOLOv8 head detection, then generates interactive HTML heatmap reports with 10-minute traffic trends, space-utilization views, and count summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to configure JF camera-based indoor traffic collection, run head detection on captures, and generate heatmap reports for space utilization and traffic review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring indoor camera monitoring can expose personal or sensitive location data.

Mitigation: Use only for authorized camera locations with appropriate notice, retention rules, and restricted access to reports, thumbnails, and summaries.

Risk: The detection model may be downloaded automatically from GitHub without a verified hash.

Mitigation: Manually install a vetted model file with a verified hash before use and avoid automatic downloads where possible.

Risk: Scheduled task text may accidentally contain real JF secrets.

Mitigation: Keep JF credentials in the managed environment and do not include real secrets in scheduled task messages.

Risk: Dependency drift can change detection behavior or security posture.

Mitigation: Pin Python dependencies and review the skill before installation or scheduled execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jftech/skills/jf-open-pro-traffic-heatmap)
- [YOLOv8 head detector repository](https://github.com/Abcfsa/YOLOv8_head_detector)
- [YOLOv8 head detector medium weights](https://github.com/Abcfsa/YOLOv8_head_detector/raw/main/medium.pt)
- [YOLOv8 head detector nano weights](https://github.com/Abcfsa/YOLOv8_head_detector/raw/main/nano.pt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON snippets; scripts produce JSON detection summaries, SQLite data, HTML reports, PNG heatmaps, and text summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports, thumbnails, summaries, and camera-derived data should be treated as sensitive operational data.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata version is 1.4.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
