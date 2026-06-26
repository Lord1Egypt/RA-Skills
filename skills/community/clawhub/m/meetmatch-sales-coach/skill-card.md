## Description: <br>
AI sales coach that sends personalized morning briefings, tracks rep patterns over time, and uses MeetMatch's ML predictions to make your agent smarter about sales outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brettonb](https://clawhub.ai/user/brettonb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales reps and sales managers use this skill to prepare for meetings, review risk-scored schedules, receive personalized coaching nudges, and generate morning or on-demand briefings from MeetMatch sales outcome data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive employee performance data and customer-call context. <br>
Mitigation: Confirm MeetMatch data handling, access controls, and retention policies before enabling it for a sales organization. <br>
Risk: Persistent rep memory may create long-running profiles of employee behavior. <br>
Mitigation: Define administrator controls for visibility, deletion, retention, and opt-out before broad deployment. <br>
Risk: Scheduled morning briefings may send sales and performance information by email. <br>
Mitigation: Require opt-in recipients, verified delivery addresses, and review of what content is included in outbound briefings. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/brettonb/meetmatch-sales-coach) <br>
- [MeetMatch](https://www.meetmatch.ai) <br>
- [OpenClaw Integration Guide](https://www.meetmatch.ai/integrations/openclaw) <br>
- [Interactive Demo](https://www.meetmatch.ai/demo/clawcon) <br>
- [MeetMatch OpenClaw API](https://www.meetmatch.ai/api/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Conversational text or Markdown briefings generated from MeetMatch API data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MEETMATCH_API_KEY and MEETMATCH_ORG_ID; scheduled briefings may be delivered by email.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
