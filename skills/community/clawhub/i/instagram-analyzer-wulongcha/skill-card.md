## Description:

Analyze Instagram profiles and posts with engagement metrics, view counts, follower ratios, and Reels-focused analytics with JSON and CSV export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wulooongcha](https://clawhub.ai/user/wulooongcha)

### License/Terms of Use:

MIT-0

## Use Case:

Social media analysts, marketers, and developers use this skill to inspect public Instagram profile and post performance, especially Reels engagement, and export metrics for downstream review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill drives a browser to user-supplied Instagram URLs or profiles.

Mitigation: Use only public Instagram URLs and profiles you trust, and run the skill in an isolated environment.

Risk: The security review notes that output paths can be derived from unsanitized usernames.

Mitigation: Restrict output to a dedicated directory and sanitize or validate usernames before relying on generated paths.

Risk: The artifact includes empty Instagram credential fields and the security guidance warns against personal credential use.

Mitigation: Avoid providing personal Instagram credentials unless credential handling has been reviewed and documented.

Risk: Dependencies are specified as version ranges rather than pinned exact versions.

Mitigation: Pin and review dependencies before deployment in controlled or production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wulooongcha/skills/instagram-analyzer-wulongcha)
- [Publisher profile](https://clawhub.ai/user/wulooongcha)

## Skill Output:

**Output Type(s):** [text, JSON, CSV, shell commands, configuration]

**Output Format:** [Command guidance plus JSON, CSV, and text file exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes profile and post analysis files, batch results, and Reels link lists under the configured data directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
