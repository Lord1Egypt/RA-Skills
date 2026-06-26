## Description: <br>
Military Bidding Email fetches military procurement opportunities from three sources, generates Excel reports, and sends the report by SMTP email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangpengle](https://clawhub.ai/user/zhangpengle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams tracking military procurement opportunities use this skill to generate dated email reports, optionally filtered by keywords or sent to a test recipient. It is intended for the military procurement reporting workflow described by the skill, not as a general email client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends email using local SMTP credentials and configured recipients. <br>
Mitigation: Use a dedicated SMTP account and verify EMAIL_TO, EMAIL_CC, and test recipient overrides before each run. <br>
Risk: The skill depends on a missing or unreviewed milb_fetcher component for data collection. <br>
Mitigation: Install only when that dependency is trusted and review fetched report content before relying on or forwarding it. <br>
Risk: Configuration is loaded from local .env files and may be picked up from the current working directory. <br>
Mitigation: Run the skill from a controlled directory and avoid directories containing unrelated .env files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangpengle/military-bidding-email) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zhangpengle) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Text] <br>
**Output Format:** [CLI-driven report generation with an Excel attachment and SMTP email content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local EMAIL_* SMTP and recipient configuration; depends on milb-email and milb-fetcher command availability.] <br>

## Skill Version(s): <br>
0.2.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
