## Description: <br>
Enable agents and skills to challenge users for fresh two-factor authentication proof (TOTP or YubiKey) before executing sensitive actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryancnelson](https://clawhub.ai/user/ryancnelson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agents use this skill to require fresh identity proof before deployments, financial actions, data exports, administrative changes, or other approval-gated operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a security gate with review-worthy bypass capabilities, including utilities that can produce current TOTP codes. <br>
Mitigation: Remove or restrict get-current-code.sh and the totp.mjs current command before using the skill for real approval gates. <br>
Risk: Plaintext OTP secrets in config files or shell profiles can weaken the verification model if the host or agent environment is compromised. <br>
Mitigation: Store OTP and YubiKey secrets in a dedicated secret manager and restrict local filesystem permissions. <br>
Risk: The default verification lifetime may be too long for highly sensitive workflows. <br>
Mitigation: Shorten OTP_INTERVAL_HOURS and expire verification state regularly for sensitive approvals. <br>
Risk: OTP_FAILURE_HOOK can execute arbitrary commands on verification failure events. <br>
Mitigation: Enable OTP_FAILURE_HOOK only with a trusted, fixed script controlled by the operator. <br>
Risk: YubiKey mode sends validation requests to Yubico Cloud. <br>
Mitigation: Review the external validation data flow before enabling YubiKey mode in regulated or offline environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryancnelson/otp-challenger) <br>
- [Project homepage](https://github.com/ryancnelson/otp-challenger) <br>
- [Yubico OTP documentation](https://developers.yubico.com/OTP/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text status messages and Markdown documentation with bash and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns shell exit codes, records local verification state, and may call Yubico Cloud when YubiKey mode is enabled.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
