## Description:

将会议逐字稿或录音转写文本转化为手机端可直接转发的 SVG 会议纪要卡片，并自动转为 PNG 方便分享。

This skill is ready for commercial/non-commercial use.

## Publisher:

[maojiebc](https://clawhub.ai/user/maojiebc)

### License/Terms of Use:

MIT

## Use Case:

External users, employees, and developers use this skill to turn meeting transcripts or speech-to-text notes into concise visual minutes that align decisions, owners, open questions, milestones, and action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes meeting transcripts that may contain sensitive business or personal information.

Mitigation: Use it only on transcripts the user is authorized to process, and redact sensitive details before creating shareable images.

Risk: The PNG converter uses local automatic execution paths for SVG rendering.

Mitigation: Review the skill before installing, avoid converting SVG files from untrusted sources, and run the converter in a pinned dependency environment without privileged accounts or broad secrets.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/maojiebc/skills/majia-meeting-svg)
- [Project Homepage](https://github.com/maojiebc/majia-meeting-svg)
- [Example Cards](https://github.com/maojiebc/majia-meeting-svg/tree/main/references/examples)
- [GitHub Releases](https://github.com/maojiebc/majia-meeting-svg/releases)
- [skills.sh Listing](https://skills.sh/maojiebc/majia-meeting-svg)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with SVG code, shell commands, and generated SVG/PNG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PNG conversion defaults to 2x scale for phone-friendly sharing.]

## Skill Version(s):

1.1.13 (source: evidence.release.version, evidence.parsed.metadata.version, SKILL.md metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
