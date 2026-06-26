## Description: <br>
Junyi Client Follow-up sends monthly child growth review questionnaires for ages 0-8, collects parent feedback, formats it for a planner, and avoids evaluation, strategy changes, report edits, and medical diagnosis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XuanranC](https://clawhub.ai/user/XuanranC) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External client-service or family-support teams use this skill to run monthly follow-up cycles: sending parent questionnaires, collecting replies, and forwarding formatted feedback to an assigned planner without making assessments or changing plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parent replies may contain sensitive child, family, school, or medical information that is forwarded to a planner. <br>
Mitigation: Use only where parents have explicitly agreed to planner forwarding, including urgent red-line escalations, and disclose that forwarding in the questionnaire flow. <br>
Risk: Misconfigured planner routing could send sensitive follow-up content to the wrong recipient. <br>
Mitigation: Configure PLANNER_CONTACT carefully and require confirmation before sending or processing replies. <br>
Risk: Full unredacted messages may share more information than needed for monthly follow-up. <br>
Mitigation: Prefer minimum-necessary sharing and edit templates or operating procedures to reduce unnecessary personal details. <br>
Risk: Group-chat use could expose child information to unintended participants. <br>
Mitigation: Avoid group-chat use and keep child-identifying information out of shared channels. <br>


## Reference(s): <br>
- [Client Questionnaire](references/client-questionnaire.md) <br>
- [Client Rules](references/client-rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/XuanranC/junyi-client-followup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and plain-text message templates with structured planner handoff summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces parent questionnaires, reminder text, planner-forwarded summaries, and state-transition guidance; it does not produce assessments or plan edits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
