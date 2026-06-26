## Description: <br>
Otpforge helps agents manage local TOTP/2FA accounts, store base32 secrets in a local JSON vault, and display current codes through a CLI or optional Tkinter GUI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ordsbot](https://clawhub.ai/user/ordsbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use Otpforge to manage local OTP vault entries and retrieve current TOTP codes from the command line or a simple desktop GUI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local vault contains authentication secrets that can be used to generate 2FA codes. <br>
Mitigation: Install and use the skill only on trusted devices with protected local storage; avoid shared or synced vault paths. <br>
Risk: Command-line secrets, displayed codes, and copied codes are sensitive credentials. <br>
Mitigation: Avoid use in shared terminals or screen-sharing sessions, clear copied codes when finished, and prefer an encrypted password manager for high-value accounts. <br>


## Reference(s): <br>
- [Otpforge ClawHub page](https://clawhub.ai/ordsbot/otpforge) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline shell commands and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May display time-limited TOTP codes and local vault management commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
