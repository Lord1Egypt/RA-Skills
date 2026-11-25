## Description:

当用户需要做好看视频选题、短视频内容方向规划或竞品角度复盘时使用。基于用户提供的主题或视频链接，整理相关作品、标题角度与评论反馈，输出带样本依据的选题清单。来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者和营销人员可用它规划好看视频选题、整理短视频内容方向，并复盘竞品角度。技能根据用户给出的主题或视频链接汇总作品、标题角度和评论反馈，形成带样本依据的选题清单。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a changeable CLI package, so a compromised package update could access credentials or data available in its execution environment.

Mitigation: Review the package and updates before installation, and run it only in an environment with the credentials and data needed for the task.

Risk: Topics and video links submitted for analysis are sent to SocialDataX.

Mitigation: Avoid submitting sensitive topics or links, and confirm the service is appropriate for the material before making a request.

## Reference(s):

- [SocialDataX skill and API access](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill page](https://clawhub.ai/devinchen2014/skills/haokan-topic-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis]

**Output Format:** [Markdown selection list with topic ideas, audience, angle, suggested title, priority, rationale, and sample video links or IDs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates topic clues, video facts, and comment feedback; states sample counts and missing information when available.]

## Skill Version(s):

0.1.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
