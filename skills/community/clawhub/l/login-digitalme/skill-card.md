## Description: <br>
This skill helps agents send SMS verification codes and complete phone-based login or registration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guolai806](https://clawhub.ai/user/guolai806) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and support agents use this skill when a workflow needs to send an SMS verification code and authenticate or register a phone-number user. The skill expects a configured SMS_LOGIN_BASE_URL, curl, jq, and explicit user-provided phone and SMS code values. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Phone login factors may be sent to an unclear raw IP endpoint. <br>
Mitigation: Install only after verifying that SMS_LOGIN_BASE_URL points to the intended authentication service over HTTPS. <br>
Risk: Phone numbers, SMS codes, bearer tokens, and cookies are sensitive authentication material. <br>
Mitigation: Avoid logging full responses, redact token and cookie values, and show at most a truncated token when output is needed. <br>
Risk: Repeated or automated SMS-code attempts could create account-abuse or rate-limit issues. <br>
Mitigation: Require explicit user-provided phone and SMS code values, validate phone format, respect the 60-second resend rule, and do not brute force verification codes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guolai806/login-digitalme) <br>
- [Publisher profile](https://clawhub.ai/user/guolai806) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and response-handling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, SMS_LOGIN_BASE_URL, and user-provided phone number and SMS code; token and cookie values should be redacted in output.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
