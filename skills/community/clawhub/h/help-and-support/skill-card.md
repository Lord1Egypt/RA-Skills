## Description: <br>
Get contextual help, onboarding guidance, issue reporting, and app version support for the Finance District agent wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rachidjarray-hk-qa-fdt](https://clawhub.ai/user/rachidjarray-hk-qa-fdt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External wallet users and support agents use this skill to answer wallet questions, guide onboarding, submit issue reports, and collect app version details for troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Issue reports can accidentally include sensitive wallet or account information. <br>
Mitigation: Review report text before submission and do not include seed phrases, private keys, passwords, API tokens, recovery details, unnecessary wallet identifiers, or sensitive screenshots. <br>
Risk: Submitting an issue report requires authentication. <br>
Mitigation: Check authentication status with `fdx status` before reporting an issue; use unauthenticated help and onboarding flows when the user only needs guidance. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Finance District help, onboarding, issue-reporting, version, and status commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
