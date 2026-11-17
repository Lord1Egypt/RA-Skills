## Description:

Searches LinkedIn-sourced people data by name, company, title, industry, geography, and contact-availability filters for recruiting, sales prospecting, and B2B lead discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, sourcers, sales teams, and B2B lead builders use this skill to find LinkedIn profiles and enrich candidate or prospect lists with role, company, region, industry, and contact-availability signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API calls and recharge actions can incur costs.

Mitigation: Confirm billable actions before execution, check current pricing through the documented price source, and get explicit approval before large result requests.

Risk: API keys may be stored in a local plaintext environment file.

Mitigation: Prefer a managed secret or environment variable, keep any local credential file owner-only, and do not print the credential file contents.

Risk: People-search results may include personal, contactability, or demographic data retained in local task outputs.

Mitigation: Confirm legal, privacy, and outreach obligations before use, limit collection to the needed fields, and delete stored task results when no longer needed.

Risk: The skill depends on Upkuajing network services for search, pricing, account, reporting, and version checks.

Mitigation: Install and run it only where calls to the Upkuajing service are approved and trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/linkedin-person-search-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer platform](https://developer.upkuajing.com/)
- [LinkedIn person list API reference](references/linkedin-person-list-api.md)
- [Skill error report API reference](references/skill-error-report-api.md)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON responses from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce task IDs, local result files, downloadable result URLs, fee information, and account guidance from paid Upkuajing API calls.]

## Skill Version(s):

1.0.3 (source: server release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
