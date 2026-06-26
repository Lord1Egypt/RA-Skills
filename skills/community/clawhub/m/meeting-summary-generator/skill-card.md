## Description: <br>
AI-powered meeting summary generator that converts meeting notes into professional summaries and action items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icepopma](https://clawhub.ai/user/icepopma) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, teams, and professionals use this skill to turn raw meeting notes into structured summaries with decisions, action items, discussion points, attendees, and next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal runs attempt an automatic 0.003 USDT SkillPay charge using an embedded merchant key unless test mode is used. <br>
Mitigation: Review the billing behavior before installing, use --test for dry runs, and avoid setting SKILLPAY_MERCHANT_KEY unless payment use is intentional. <br>
Risk: Private meeting notes are processed by the configured OpenClaw/Sloan agent. <br>
Mitigation: Submit sensitive meeting content only when the local OpenClaw/Sloan setup and data handling are approved for that content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/icepopma/meeting-summary-generator) <br>
- [Project repository listed in skill docs](https://github.com/icepopma/meeting-summary-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Markdown meeting summary printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts inline notes or a notes file plus optional title, date, and test mode.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
