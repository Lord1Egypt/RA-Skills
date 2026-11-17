## Description:

每日检查 OpenClaw 最新版本和 Release Note，分析更新必要性并推送详细更新建议给用户，不主动执行更新。

This skill is ready for commercial/non-commercial use.

## Publisher:

[noir-hedgehog](https://clawhub.ai/user/noir-hedgehog)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to check whether a newer OpenClaw release is available, review release notes, and receive an update recommendation through Feishu or a configured messaging tool. It reports update guidance only and does not perform updates automatically.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled checks or messaging integrations may send version and release-summary information through Feishu or another configured tool.

Mitigation: Configure the schedule and messaging destination deliberately, and keep the workflow limited to reporting rather than automatic updating.

Risk: Release-note analysis may produce incomplete or incorrect update recommendations.

Mitigation: Review the linked release notes and breaking-change details before acting on the recommendation.

## Reference(s):

- [OpenClaw Releases](https://github.com/openclaw/openclaw/releases)
- [ClawHub Skill Page](https://clawhub.ai/noir-hedgehog/skills/openclaw-update-check)
- [Publisher Profile](https://clawhub.ai/user/noir-hedgehog)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown update report with version comparison, release-note summary, and recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu or message delivery content; limited to reporting and update guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
