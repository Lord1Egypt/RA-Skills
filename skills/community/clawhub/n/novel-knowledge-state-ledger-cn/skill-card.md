## Description:

输入按故事顺序排列的场景、事实编号，以及人物亲历、被告知、推测或使用事实的非空原文证据，输出人物×事实知情矩阵、首次得知场景、确信/猜测/未知状态与提前使用位置。适用于小说跨场景连续性核对；缺少顺序或证据时先索取材料，推测记为猜测、无人物证据记为未知，且不把读者所知计入人物。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

小说作者和编辑可用它整理人物对故事事实的知情状态，并核查人物是否在获得证据前使用信息。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation instructions fetch an externally hosted skill without pinning its version.

Mitigation: Review the release being installed and use a pinned version where supported.

Risk: The security report says two scripts were only partly inspected, so it does not establish the package’s complete behavior.

Mitigation: Review the full release contents before running the skill.

## Reference(s):

- [ClawHub release](https://clawhub.ai/xxjrq/skills/novel-knowledge-state-ledger-cn)
- [Source repository](https://github.com/xxjrq/novel-knowledge-state-ledger-cn)
- [Story-skills revision continuity reference](https://github.com/danjdewhurst/story-skills/blob/main/skills/revision-continuity/SKILL.md)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON knowledge matrix and early-use findings; text request when required input is missing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports up to 20 scenes, 30 facts, and 10 characters; requires scenes in story order and non-empty quoted character evidence.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata, manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
