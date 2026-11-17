## Description:

Retrieves shareholder records and ownership details for a company ID from UpKuaJing's global company database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, industry analysts, sales teams, and risk management specialists use this skill to inspect shareholder rosters, ownership ratios, and related equity-structure details for due diligence, investment research, competitor analysis, and controller checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs paid API calls and includes account top-up helper commands.

Mitigation: Before any fee-incurring call, inform the user that fees apply, check current pricing through the provided price source or price command, and wait for explicit confirmation in a separate response.

Risk: The skill can read or write UPKUAJING_API_KEY in a local plaintext file at ~/.upkuajing/.env.

Mitigation: Prefer a safer secret mechanism such as an environment variable or secret manager; if the local file is used, ensure it is owner-only readable and never print its contents.

Risk: Confirmed error reports are sent to the UpKuaJing platform and may include request context.

Mitigation: Submit error reports only after user confirmation and avoid including sensitive business, account, or credential data in report context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/global-company-shareholder)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
- [Company Shareholder List API](references/company-shareholder-list-api.md)
- [Skill Error Report API](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands, Guidance]

**Output Format:** [JSON API responses with concise natural-language guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a company ID and UPKUAJING_API_KEY; successful shareholder queries include result data, fee details, and a request identifier.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
