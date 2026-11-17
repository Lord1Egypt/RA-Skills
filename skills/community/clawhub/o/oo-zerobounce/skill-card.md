## Description:

Operate ZeroBounce through an OOMOL-connected account to validate email addresses, review account data, and manage custom filter rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use the skill to validate email addresses, review activity, usage, and credit balance, and manage custom filter rules in ZeroBounce.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses a remote installer whose behavior has not been verified, and the CLI can persistently install additional agent skills.

Mitigation: Review and install a verified oo CLI release separately. If you do not want additional skills installed, use the publisher-documented OO_SKILLS_SYNC_DISABLED=1 setting.

Risk: Using the connected service sends submitted email addresses to ZeroBounce through OOMOL, which may have privacy or data-handling implications.

Mitigation: Confirm that the intended email data may be processed through this OOMOL connection before running validation or activity actions.

Risk: Creating or updating a custom filter rule changes ZeroBounce account state.

Mitigation: Review the exact filter rule and its effect with the user and obtain confirmation before running the write action.

## Reference(s):

- [ZeroBounce](https://www.zerobounce.net)
- [ZeroBounce Email Validation API Quickstart](https://www.zerobounce.net/docs/email-validation-api-quickstart/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON action responses and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can return email validation, account, activity, and filter-rule data; filter-rule changes require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
