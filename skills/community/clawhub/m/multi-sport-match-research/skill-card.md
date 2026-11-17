## Description:

Compare public fixtures, live scores, match statistics, standings, and head-to-head records using Crawlora Flashscore and LiveScore tools. Use for multi-sport score checks, a sourced match preview or recap, or reconciling different scoreboard providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can check fixtures, live scores, statistics, standings, and head-to-head records across sports, then prepare sourced match previews or recaps and reconcile provider differences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill requires a Crawlora API key, and the partial ClawScan could not resolve one local reference.

Mitigation: Review the unresolved reference and proceed only if you trust Crawlora with the API key, as ClawScan advises.

## Reference(s):

- [Endpoint reference](artifact/reference/endpoints.md)
- [ClawHub skill page](https://clawhub.ai/crawlora-org/skills/multi-sport-match-research)

## Skill Output:

**Output Type(s):** [text, markdown, analysis]

**Output Format:** [Markdown match summaries with sourced scores, status, timestamps, and provider comparisons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report unresolved provider differences and data limits; does not treat empty or failed responses as a confirmed score or cancellation.]

## Skill Version(s):

1.0.5 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
