## Description: <br>
Automate NYC 311 service request filing by browsing the 311 portal with Playwright. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pranjalminocha](https://clawhub.ai/user/pranjalminocha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to prepare, preview, and optionally submit NYC 311 service requests through browser automation when a complaint needs end-to-end filing assistance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit a real NYC 311 report when run with the submit option. <br>
Mitigation: Run the dry run first, inspect the generated screenshot, and submit only after the user confirms the complaint details are accurate. <br>
Risk: Reporter contact details and address data may be stored in assets/config.json or passed through command arguments. <br>
Mitigation: Use only user-approved contact details, avoid storing real personal data unless needed, and remove or replace sensitive values after the report is complete. <br>
Risk: Screenshots saved under /tmp may contain personal data or complaint details. <br>
Mitigation: Delete /tmp/311_*.png screenshots after review or after the report workflow is complete. <br>


## Reference(s): <br>
- [NYC 311 Portal](https://portal.311.nyc.gov/) <br>
- [ClawHub skill page](https://clawhub.ai/pranjalminocha/nyc-311-reporter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local screenshots under /tmp for user review during dry runs or submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
