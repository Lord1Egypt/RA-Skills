## Description:

Helps users claim Meituan promotional coupons, open related activity links, and set daily coupon reminders after phone and SMS authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meituan-union](https://clawhub.ai/user/meituan-union)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an agent to authenticate a Meituan account, claim available coupons, view related promotional activity links, manage coupon history and reminders, and run explicit diagnostics when troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Meituan phone number, SMS code, and account token for coupon claiming.

Mitigation: Install only when that credential access is acceptable, and use the logout or device-clear flows when access should be removed.

Risk: Security evidence says the skill under-discloses credential handling and makes misleading local-only privacy statements.

Mitigation: Review and correct consent text and data-flow disclosures before deployment.

Risk: Security evidence says some authentication requests disable TLS certificate checks.

Mitigation: Require TLS verification on authentication requests before treating the release as low-risk.

Risk: Security evidence says tokens are exposed through script output or command-line arguments and logs are decryptable.

Mitigation: Redact credential outputs, avoid passing tokens through command arguments, minimize retained logs, and restrict local file permissions.

Risk: Security evidence says the skill can set reminders and run update or diagnostic flows.

Mitigation: Keep reminder, update, and diagnostic actions user-initiated or explicitly confirmed, and review their scope before enabling them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meituan-union/skills/meituan-union-coupon-skill)
- [Skill service rules](references/terms-of-service.md)
- [Diagnostic guide](references/DOCTOR.md)
- [Meituan user service agreement](https://rules-center.meituan.com/rule-detail/4/1)
- [Meituan privacy policy](https://rules-center.meituan.com/m/detail/guize/2)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Chinese user-facing messages, Markdown coupon tables, JSON script results, and shell command invocations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include coupon records, activity links, authentication status, reminder settings, and diagnostic output; credential-bearing output should be redacted.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact SKILL.md mentions 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
