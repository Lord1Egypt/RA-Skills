## Description:

Monitor influencer campaigns across TikTok, Instagram, and YouTube by creating and managing monitor tasks, pulling metrics, downloading tracked assets, and supporting post-campaign reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengyu-xixihaha](https://clawhub.ai/user/chengyu-xixihaha)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing analysts and campaign operators use this skill to operate social video monitoring tasks and turn TikTok, Instagram, and YouTube metrics into campaign review notes, anomaly checks, and optimization recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Campaign identifiers, creator or video identifiers, task data, credentials, and a stable install ID may be sent to configured remote endpoints.

Mitigation: Review the skill before installing, use a trusted HTTPS environment configuration, and only run it when this data sharing is acceptable.

Risk: The stable install ID can allow cross-session correlation.

Mitigation: Delete ~/.scrumball_install_id when correlation across sessions is not desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chengyu-xixihaha/skills/influencer-campaign-monitoring)
- [API Index](artifact/references/api-index.md)
- [Request and Response Guide](artifact/references/request-response.md)
- [Operation Manifest](artifact/references/operations.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or structured text summarizing task status, performance trend, anomalies, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include campaign, creator, video, task, metric, and tracked asset identifiers returned by the configured API gateway.]

## Skill Version(s):

1.0.3 (source: evidence.release.version and config.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
