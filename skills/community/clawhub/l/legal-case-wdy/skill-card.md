## Description:

Searches Wendaoyun for legal provisions and similar cases based on a user's dispute description, then formats retrieved laws, case summaries, and optional next-step analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rose-develop](https://clawhub.ai/user/rose-develop)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to retrieve legal provisions and similar case examples for preliminary dispute triage. It supports legal search and formatted case summaries, but users should review results before relying on them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive dispute details may be sent to the Wendaoyun third-party API.

Mitigation: Use minimal, anonymized search terms and omit names, IDs, addresses, account details, medical details, and confidential facts.

Risk: Legal search results and suggested next steps may be incomplete or jurisdiction-specific.

Mitigation: Review retrieved laws and cases before relying on them, and use qualified legal advice for real disputes.

Risk: The skill depends on a user-provided WENDAOYUN_API_KEY for API access.

Mitigation: Store the API key only in the environment, avoid sharing it in prompts or logs, and revoke it through Wendaoyun if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rose-develop/skills/legal-case-wdy)
- [Wendaoyun API portal](https://open.wendaoyun.com/home)
- [Wendaoyun get-laws endpoint](https://h5.wintaocloud.com/prod-api/api/invoke/get-laws)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, API Calls, Shell commands, Configuration guidance]

**Output Format:** [Markdown with legal provisions, similar case summaries, optional analysis, and setup shell commands when the API key is missing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WENDAOYUN_API_KEY; sends user-provided legal search terms to the Wendaoyun third-party API; top_k defaults to 3 and is capped at 5.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
