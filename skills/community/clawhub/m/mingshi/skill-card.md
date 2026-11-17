## Description:

Yunshi provides Chinese astrology and fortune-telling assistance, including BaZi, ZiWei DouShu, QiMen DunJia, I Ching divination, marriage compatibility, feng shui guidance, and daily fortune messages without external API dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External users use Yunshi as a personal Chinese astrology assistant for chart readings, fortune analysis, divination, compatibility checks, feng shui recommendations, and scheduled daily fortune messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local profile and push data can include names, birth details, family data, preference history, and scheduled fortune messages.

Mitigation: Use the skill only in private workspaces, restrict access to data/profiles and data/push-log.json, and remove stored profiles when no longer needed.

Risk: Profile and push scripts may allow overbroad local file access through userId path handling.

Mitigation: Constrain userId values to safe identifiers and review the path handling before enabling registration, profile, or push features in shared or multi-user environments.

Risk: Scheduled push prompts are persisted and built from user profile data.

Mitigation: Review scheduled message content before enabling recurring delivery, keep generated prompts out of shared logs, and use dry-run or test modes before live push delivery.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiajiaoy/skills/mingshi)
- [README](README.md)
- [User Registration Flow](docs/注册流程.md)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text or Markdown responses with command snippets and local JSON profile or scheduling configuration when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese and English responses; scripts can read and write local profile, preference, and push-log data.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact package and docs show 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
