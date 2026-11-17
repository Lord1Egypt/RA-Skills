## Description:

Generate a grounded nuclear energy policy brief from live news using Apify + Contextual.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ab-naidu](https://clawhub.ai/user/ab-naidu)

### License/Terms of Use:

MIT-0

## Use Case:

Policy analysts and energy policy teams use this skill to turn recent public nuclear energy policy and regulatory news into a concise, source-grounded brief with changes, risks, and recommended actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search topic, audience, and fetched article content are sent to Apify and Contextual.

Mitigation: Avoid sensitive queries, use scoped API keys with spending limits, and keep credentials out of commits and logs.

Risk: Generated briefs can be influenced by incomplete, stale, or misleading public news snippets.

Mitigation: Treat the brief as a draft and verify important claims against the cited source links before acting on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ab-naidu/skills/global-nuclear-brief)
- [Project repository](https://github.com/ab-naidu/global-nuclear-brief)
- [Apify dataset items API endpoint](https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items)
- [Contextual generation API endpoint](https://api.contextual.ai/v1/generate)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown-style policy brief with source titles and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIFY_API_TOKEN and CONTEXTUAL_API_KEY; generated from live public news results and grounded source snippets.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
