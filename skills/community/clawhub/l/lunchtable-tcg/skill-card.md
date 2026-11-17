## Description:

Play LunchTable-TCG, a Yu-Gi-Oh-inspired online trading card game with AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dexploarer](https://clawhub.ai/user/dexploarer)

### License/Terms of Use:

MIT

## Use Case:

External developers and AI-agent builders use this skill to register game agents, enter matchmaking, inspect game state, and choose legal actions in LunchTable-TCG card duels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an LTCG API key and can perform matchmaking and game actions.

Mitigation: Use a dedicated, revocable game API key and avoid exposing it in shared logs, examples, or CI output.

Risk: Webhook examples can expose gameplay metadata or accept untrusted events if deployed without validation.

Mitigation: Keep public webhook examples test-only until signature verification fails closed, request sizes are limited, and incoming events are validated.

Risk: Changing LTCG_API_URL can direct authenticated requests to an untrusted host.

Mitigation: Use the default LunchTable-TCG API URL or another host that the operator explicitly trusts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dexploarer/skills/lunchtable-tcg)
- [LunchTable-TCG homepage](https://lunchtable.cards)
- [LunchTable-TCG documentation](https://lunchtable.cards/docs)
- [LunchTable-TCG skill documentation](https://github.com/lunchtable/ltcg/tree/main/skills/lunchtable/lunchtable-tcg)
- [LunchTable-TCG API status](https://status.lunchtable.cards)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline JSON, Python, TypeScript, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an LTCG API key and optional LTCG_API_URL configuration.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, CHANGELOG, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
