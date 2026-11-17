## Description:

Searches Kuaishou works by keyword and helps an agent return sorted, filtered result tables with engagement metrics and links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, operations analysts, brands, MCNs, e-commerce sellers, and individual users use this skill to discover Kuaishou works by topic, compare engagement metrics, browse filtered results, and optionally subscribe to daily keyword updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and filter settings are sent to RedFox for Kuaishou search.

Mitigation: Enable the skill only when users are comfortable sharing those query details with RedFox and have reviewed the RedFox API key source, scope, expiration, and revocation options.

Risk: The skill can create recurring daily scheduled searches with insufficiently documented review, cancellation, and containment controls.

Mitigation: Before enabling a subscription, confirm the exact keyword, schedule, storage location for the task, cancellation path, and audit process.

Risk: A REDFOX_API_KEY is required for operation and could be exposed if mishandled.

Mitigation: Store the key in the agent environment or approved configuration store, and avoid hardcoding or printing it in prompts, code, logs, or output files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/kuaishou-search)
- [RedFoxHub](https://redfox.hk)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFox Kuaishou keyword search API endpoint](https://redfox.hk/story/api/ks/search/keywordSearchWork)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON search results and Markdown response tables with optional shell and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY. Search requests send keywords and filters to RedFox; data is described as updated daily at 06:00, and subscriptions run daily at 09:00 when enabled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
