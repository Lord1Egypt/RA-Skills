## Description: <br>
Health Buddy Pro helps an agent estimate meal nutrition from photos or text, track hydration, supplements, activity, custom wellness metrics, and produce daily or weekly summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill for conversational nutrition and wellness tracking, including photo-based meal logging, goal check-ins, hydration tracking, supplement reminders, activity logging, and summary reporting. It is informational only and is not a medical device, healthcare provider, or substitute for professional medical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive wellness information while the server security summary reports incomplete and partly conflicting privacy and storage disclosures. <br>
Mitigation: Review storage, consent, retention, deletion, export, and cloud-storage behavior before entering personal health data. <br>
Risk: Photo-based calorie and macro estimates can be inaccurate and are not appropriate for medical decisions. <br>
Mitigation: Treat estimates as informational, verify nutrition-label values when available, and consult a qualified healthcare professional for medical or dietary decisions. <br>
Risk: Setup and initialization commands create local data files that may contain sensitive health information. <br>
Mitigation: Review commands before execution, keep generated data directories private, and use local device protections such as disk encryption. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nollio/normieclaw-health-buddy-pro) <br>
- [Publisher profile](https://clawhub.ai/user/nollio) <br>
- [README](artifact/README.md) <br>
- [Security audit notes](artifact/SECURITY.md) <br>
- [Setup prompt](artifact/SETUP-PROMPT.md) <br>
- [Dashboard specification](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Conversational text and Markdown summaries with JSON configuration and log updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose shell commands for setup and local data initialization; nutrition estimates are approximate unless copied from a nutrition label.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
