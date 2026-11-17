## Description:

Searches recent WeChat Official Account articles with 5,000+ reads by keyword, ranks results by relevance, heat, and timeliness, and helps content creators find trend and topic inspiration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, WeChat operators, and brand teams use this skill to search recent viral WeChat articles, compare content trends, and schedule recurring topic checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact exposes a credential-like API key.

Mitigation: The publisher should remove and rotate the exposed key; users should configure their own scoped REDFOX_API_KEY.

Risk: Search terms are sent to the RedFox service.

Mitigation: Use the skill only when sending those terms to RedFox is acceptable, and avoid sensitive queries.

Risk: Optional HTML reports may be unsafe to open until escaping is fixed.

Mitigation: Avoid opening generated HTML reports unless the HTML escaping issue is resolved.

Risk: Recurring subscriptions can store search parameters and run on a schedule.

Mitigation: Review the recurrence, push time, and stored query details before creating a calendar subscription.

## Reference(s):

- [Data format reference](references/gzh_trend_data_format.md)
- [ClawHub skill release page](https://clawhub.ai/yuanyi-github/skills/gzh-explosive-content-detector)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance, files]

**Output Format:** [Markdown tables and prompts, JSON from stdout, and optional HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; can create recurring calendar subscriptions when the user chooses scheduled pushes.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
