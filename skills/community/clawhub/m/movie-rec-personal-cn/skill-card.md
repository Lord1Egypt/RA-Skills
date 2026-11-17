## Description:

猫眼电影个性化推荐系统，每周抓取中国大陆新上映和即将上映电影，基于用户观影偏好档案排序推荐并生成飞书周报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[advnljs](https://clawhub.ai/user/advnljs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect current Maoyan movie data, compare it with a local viewing-preference profile, and generate a structured Chinese movie recommendation report for Feishu delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a local movie preference profile that may contain personal viewing notes.

Mitigation: Keep sensitive personal notes out of profile.json and review profile updates before allowing the agent to write them.

Risk: The package references profile-template.json, but security evidence says that template was not present in the inspected package.

Mitigation: Create and review profile.json manually before scheduled runs, and verify required preference fields are present.

Risk: Recommendations depend on current Maoyan data and may be incomplete if external movie requests fail.

Mitigation: Review generated recommendations before acting on them and rerun collection if a report appears incomplete.

Risk: Configured delivery can send generated recommendations to Feishu.

Mitigation: Confirm the Feishu destination and report content before enabling scheduled delivery.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/advnljs/skills/movie-rec-personal-cn)
- [Maoyan Now Showing API](https://m.maoyan.com/ajax/movieOnInfoList)
- [Maoyan Coming Soon API](https://m.maoyan.com/ajax/comingList?ci=10&token=&limit=100)
- [Maoyan Movie Detail API](https://m.maoyan.com/ajax/detailmovie?movieId={movie_id})

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown recommendation report with JSON movie data and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce tiered recommendations and Feishu-ready weekly reports from the user's local profile.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
