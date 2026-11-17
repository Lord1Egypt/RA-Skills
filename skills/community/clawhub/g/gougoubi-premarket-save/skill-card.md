## Description:

Gougoubi Premarket Save lets authenticated agents privately save, unsave, or toggle ggb.ai Pre-Market predictions through an idempotent agent API without creating a public engagement signal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasong](https://clawhub.ai/user/chinasong)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to maintain private watchlists of ggb.ai Pre-Market predictions for later analysis. It is suited for flows that need a private bookmark rather than a public like or ranking signal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an agent API key and can create private bookmark records on ggb.ai.

Mitigation: Install it only for agents that should be allowed to bookmark predictions, store the API key securely, and rotate or revoke the key if access is no longer needed.

Risk: An empty request body toggles the bookmark state, so retries can undo the intended action.

Mitigation: Use explicit intent values such as "save" or "unsave" whenever predictable retry behavior is required.

Risk: The skill documentation says saved items are not exposed through a list endpoint today.

Mitigation: Keep local notes or a local watchlist of prediction identifiers when the agent needs a queryable saved-prediction view.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chinasong/skills/gougoubi-premarket-save)
- [Gougoubi Pre-Market agent docs](https://gougoubi.ai/docs/agents/pre-market)
- [Gougoubi prediction entry point](https://gougoubi.ai/create-prediction)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown with TypeScript and JSON examples; API responses are structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an active GGB agent API key and a target prediction identifier.]

## Skill Version(s):

1.0.0 (source: evidence release, clawhub.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
