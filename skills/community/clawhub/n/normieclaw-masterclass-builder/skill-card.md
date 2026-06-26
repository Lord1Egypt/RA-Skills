## Description: <br>
Create personalized multi-day masterclasses on any topic by designing custom curricula, generating daily lessons with exercises, tracking progress, and adapting difficulty for each learner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create, continue, and manage personalized multi-day learning courses on a chosen topic. The skill generates syllabi, daily Markdown lessons, exercises, homework, progress dashboards, and optional scheduled-delivery setup guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and updates local course files under masterclasses/. <br>
Mitigation: Install only if local course-file creation is acceptable, and review generated course content before relying on it. <br>
Risk: The skill may suggest an OpenClaw cron command for scheduled lesson delivery. <br>
Mitigation: Review any scheduled-delivery cron command before adding it. <br>
Risk: Homework notes and progress files may contain user-provided personal details. <br>
Mitigation: Avoid storing secrets or highly sensitive personal details in homework notes or course progress. <br>


## Reference(s): <br>
- [Curriculum Templates](references/curriculum-templates.md) <br>
- [Lesson Format Template](references/lesson-format.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/nollio/normieclaw-masterclass-builder) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown lessons and syllabi, JSON progress files, concise text responses, and optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local course data under masterclasses/ when used as directed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
