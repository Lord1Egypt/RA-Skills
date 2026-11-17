## Description:

Enables agents and skills to challenge users for fresh two-factor authentication proof with TOTP or YubiKey before sensitive actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryancnelson](https://clawhub.ai/user/ryancnelson)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to add TOTP or YubiKey checks before sensitive agent actions such as deployments, financial operations, data access, admin changes, and change-control workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security model is too broad for high-risk actions when used as strong per-action approval.

Mitigation: Bind verification to a specific user, session, and action before relying on it for deployments, payments, admin changes, or secret release.

Risk: OTP seeds and YubiKey credentials can be exposed if stored in broad environment files or shell profiles.

Mitigation: Store secrets in a dedicated secrets manager or tightly scoped configuration, and avoid broad shell-profile exports.

Risk: OTP_FAILURE_HOOK can execute arbitrary shell commands on verification failures.

Mitigation: Leave OTP_FAILURE_HOOK unset unless the hook target is tightly controlled and reviewed.

Risk: Reusable verification windows can remain valid beyond a single sensitive action.

Mitigation: Shorten or constrain the verification window for high-risk workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryancnelson/skills/otp-challenger)
- [Project homepage from ClawHub metadata](https://github.com/ryancnelson/otp-challenger)
- [RFC 6238 TOTP specification](https://tools.ietf.org/html/rfc6238)
- [Yubico OTP documentation](https://developers.yubico.com/OTP/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text status messages, Markdown guidance, shell command examples, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verification state may be recorded as local timestamp data; generated TOTP setup can include QR-code output when qrencode is installed.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
