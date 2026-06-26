## Description: <br>
用于长期记录、整理、分析用户的健康、身体状态、心理状态、生理变化、生活方式和相关个人背景信息，并支持 Apple Watch / HealthKit 数据解读、体检报告解读、慢病管理、睡眠分析、营养补剂管理、中医养生分析、长期趋势跟踪与健康决策支持。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiist007](https://clawhub.ai/user/aiist007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill as a long-term personal health assistant for organizing health records, wearable data, symptoms, lifestyle context, nutrition and supplement information, and for receiving structured wellness guidance. It combines Western medicine, Traditional Chinese Medicine, nutrition, and trend analysis perspectives while preserving medical safety boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill defaults to building a broad long-term profile from sensitive health, wearable, lifestyle, and personal context data. <br>
Mitigation: Use it only with explicit user intent, limit shared data to what is needed, and provide clear ways for users to review, correct, and delete remembered health information. <br>
Risk: HealthKit or wearable data could be accessed or interpreted without sufficient consent or clinical context. <br>
Mitigation: Require explicit confirmation before any HealthKit access and present wearable data interpretations as trend-based context rather than medical diagnoses. <br>
Risk: The skill may generate health guidance that users could mistake for clinical diagnosis, prescription, or medication-management advice. <br>
Mitigation: Preserve the skill's boundaries: do not replace clinicians, prescribe medication, change medication plans, or treat wearable data as diagnostic evidence; advise urgent care for red-flag symptoms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiist007/imperial-physician) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Analysis, Markdown] <br>
**Output Format:** [Structured Simplified Chinese Markdown with health profile updates, integrated assessments, action recommendations, nutrition and supplement guidance, and trend reminders] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill is designed to produce non-diagnostic health and wellness guidance, safety reminders, and escalation advice for urgent symptoms.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
