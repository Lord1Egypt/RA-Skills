## Description: <br>
为睡眠服务机构及从业人员提供中文问诊流程，按睡眠症状、严重度、用药情况和原因匹配助眠脑波音频链接与4周使用计划。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pvli508](https://clawhub.ai/user/pvli508) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sleep service providers use this skill to structure a short Chinese intake conversation and provide clients with a tailored sleep-audio intervention plan. It is intended as health-adjacent guidance and audio matching, not as medical diagnosis or a substitute for licensed care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat sleep-audio recommendations as medical diagnosis or a replacement for licensed care. <br>
Mitigation: Present the output as supplemental guidance, include the health warning, and refer users with severe symptoms, breathing issues, depression signs, pain, or medication questions to qualified clinicians. <br>
Risk: The skill references HTTP audio links that may be unavailable, spoofed, or altered in transit. <br>
Mitigation: Verify each audio URL before sharing it and replace HTTP links with trusted HTTPS-hosted assets where possible. <br>
Risk: Medication-related guidance could be misread as permission to change or stop prescribed sleep medication. <br>
Mitigation: Tell users not to start, stop, or adjust medication based on the skill output and to follow their prescribing clinician's advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pvli508/personalized-sleep-brainwave) <br>
- [Audio library](references/audio-library.md) <br>
- [Symptom classification](references/symptom-classification.md) <br>
- [Medication guidance](references/medication-guidance.md) <br>
- [Matching rules](references/matching-rules.md) <br>
- [Age and gender profiles](references/age-gender-profiles.md) <br>
- [Sleep audio URL prefix](http://hc.com/cusresources/sleepAudio/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with assessment questions, selected audio URLs, health notes, and a four-week usage plan] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only workflow; no code execution, persistence, credentials, or unrelated system access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
