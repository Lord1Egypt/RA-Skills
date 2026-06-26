## Description: <br>
健康饮食提醒技能。基于《中国居民膳食指南（2022）》八大准则，每日三餐+下午茶定时推荐，每次3个方案ABC供选择，饭后30分钟自动跟进记录饮食+计算热量。按膳食餐盘结构标注每餐配比，按季节推荐应季低卡食谱，含饮水管理、运动搭配、周末放纵餐、食物多样性追踪和周报打卡。支持减肥/维持/增肌三模式。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azerwang](https://clawhub.ai/user/azerwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to receive recurring meal, hydration, exercise, and weekly check-in guidance with selectable meal options and follow-up logging. It is intended for general wellness support, food variety tracking, and habit reminders rather than clinical nutrition care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring reminders may run at unintended times if cron schedules or timezone settings are accepted without review. <br>
Mitigation: Confirm the active timezone and review each scheduled reminder before enabling cron commands. <br>
Risk: Diet, water, exercise, allergy, or health-condition details shared with the agent may be stored in conversation or memory history. <br>
Mitigation: Avoid sharing sensitive medical details unless the user is comfortable with their agent environment retaining them. <br>
Risk: General meal and calorie guidance may be unsuitable for users with medical conditions or special dietary needs. <br>
Mitigation: Treat the skill as wellness support only and consult a clinician for pregnancy, lactation, diabetes, or other medical nutrition needs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/azerwang/healthy-meal-reminder) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown text with recurring reminder command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces meal choices, hydration prompts, exercise suggestions, follow-up questions, calorie estimates, and weekly check-in summaries.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
