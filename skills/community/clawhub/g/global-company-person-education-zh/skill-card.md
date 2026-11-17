## Description:

Queries Upkuajing's global company person database for a person's education history, including schools, degrees, majors, minors, GPA, summaries, and paginated results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, HR teams, hiring managers, and business users can use this skill to retrieve education-history data for a known person ID and support candidate screening, background verification, talent assessment, or B2B profile enrichment. It requires an Upkuajing API key and should only be run after confirming any paid query.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a sensitive API key and reads or writes credentials in the user's Upkuajing environment file.

Mitigation: Install only if the user trusts Upkuajing with the queried person data and API account, and do not expose the environment file contents in chat or logs.

Risk: Education lookups, pagination, recharge-order creation, and account operations can affect billing or account state.

Mitigation: Require explicit user confirmation before paid queries, recharge-order creation, or other account-affecting operations.

Risk: Diagnostic error reports may include request context related to failed skill calls.

Mitigation: Submit diagnostic reports only after explicit user confirmation and avoid including unnecessary personal, credential, or account details.

Risk: The release evidence flags hidden update-check behavior that users should review before installation.

Mitigation: Review the skill's network behavior and run it in a controlled environment before deploying it for routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/global-company-person-education-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing developer platform](https://developer.upkuajing.com/)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [Education list API reference](references/person-education-list-api.md)
- [Skill error report API reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Education-list results include request identifiers and fee information when returned by the API.]

## Skill Version(s):

1.0.4 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
