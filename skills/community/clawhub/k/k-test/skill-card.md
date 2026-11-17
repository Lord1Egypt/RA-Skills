## Description:

Search X (Twitter) posts using the xAI API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dtkien1802](https://clawhub.ai/user/dtkien1802)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search X posts through the xAI API, with filters for handles, exclusions, date ranges, image understanding, and video understanding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and filters are sent to xAI using the configured XAI_API_KEY.

Mitigation: Avoid confidential or regulated searches unless the user's xAI account, policies, and intended use permit sending that information.

Risk: Returned X search summaries and citations may be incomplete, stale, or misleading.

Mitigation: Review cited X posts and source links before relying on the output for decisions or publication.

## Reference(s):

- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search)
- [xAI Console](https://console.x.ai)
- [ClawHub skill page](https://clawhub.ai/dtkien1802/skills/k-test)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [JSON response with text, citations, search count, and token usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and XAI_API_KEY; sends search terms and filters to xAI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
