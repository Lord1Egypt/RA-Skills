## Description:

测绘/GIS 专业校招信息监控技能，帮助用户搜索、筛选、整理和推送测绘类、地理信息系统（GIS）专业校园招聘信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[5758703](https://clawhub.ai/user/5758703)

### License/Terms of Use:

MIT-0

## Use Case:

Students and job seekers in surveying, GIS, remote sensing, and related fields use this skill to find and organize campus recruiting opportunities by employer type, education requirement, deadline, location, and source link. Operators can also use it to prepare recurring job summaries after reviewing delivery settings and data freshness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence says the skill materially overstates reliable live monitoring capabilities and appears to provide mostly static examples.

Mitigation: Confirm each job listing against current source sites before relying on the results, and describe generated reports as examples unless live retrieval is independently verified.

Risk: Scheduled DingTalk delivery and file output can send information to the wrong recipient, run on the wrong cadence, or write to an unintended path if enabled without review.

Mitigation: Before enabling scheduled delivery or file writes, confirm the recipient, channel, schedule, output path, retention needs, and the process for disabling or cleaning up the job.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/5758703/skills/gis-job-monitor)
- [招聘网站汇总](references/job-sites.md)
- [测绘/GIS 用人单位名单](references/company-list.md)
- [最新测绘/GIS 校招信息](references/latest-jobs.md)
- [国聘网](https://www.iguopin.com/)
- [国聘网国企招聘专栏](https://gpxd.iguopin.com/)
- [自然资源部](http://www.mnr.gov.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown job summaries, command examples, Python-generated Word reports, and optional saved files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Job lists emphasize employer, role, degree requirement, major, location, deadline, publication date, and source link.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
