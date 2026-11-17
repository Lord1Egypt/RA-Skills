## Description:

Add SMS, WhatsApp, or Telegram OTP, 2FA, MFA, and phone verification to applications using MyOTP.App's REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myotp](https://clawhub.ai/user/myotp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to add phone verification, password reset codes, signup checks, and transaction step-up authentication through SMS, WhatsApp, or Telegram OTP flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent through account creation or paid credit top-ups.

Mitigation: Require transaction-specific approval before any registration, top-up, Stripe Link, USDC, or npx payment command is executed, including approval of amount, payment method, recipient, and spending limit.

Risk: Using the skill can send phone numbers and OTP workflow data to api.myotp.app.

Mitigation: Use the skill only for workflows where sharing phone numbers with the MyOTP service is acceptable, and keep the MYOTP_API_KEY in environment variables rather than source files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/myotp/skills/myotp)
- [MyOTP.App homepage](https://myotp.app)
- [MyOTP.App API reference](https://myotp.app/api-reference/)
- [MyOTP.App sample code](https://myotp.app/sample-code-new/)
- [MyOTP.App pricing](https://myotp.app/pricing/)
- [MyOTP.App security](https://myotp.app/security/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include REST request examples, language-specific code samples, environment-variable setup, and payment top-up steps.]

## Skill Version(s):

1.0.5 (source: evidence release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
