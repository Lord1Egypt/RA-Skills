## Description:

Uses the RollingGo CLI to search hotels, filter results, read hotel tags, and retrieve room-level pricing for hotel recommendation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longcreat](https://clawhub.ai/user/longcreat)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search hotels by destination, dates, star rating, budget, tags, brand, and distance, then compare hotel details, room availability, current prices, refund policies, and booking links through the RollingGo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run unpinned latest RollingGo packages and upgrade global installations.

Mitigation: Pin RollingGo to a reviewed version before use and avoid global upgrades during normal operation.

Risk: API keys can be exposed if passed on command lines or injected broadly into host or sandbox environments.

Mitigation: Inject RollingGo_API_KEY only for this skill where possible and avoid command-line API key arguments.

Risk: The skill depends on live RollingGo CLI calls for current hotel data and pricing.

Mitigation: Check that RollingGo_API_KEY is present before execution and present CLI/network failures as unavailable results instead of recommendations.

## Reference(s):

- [RollingGo Homepage](https://rollinggo.store)
- [RollingGo API Key Application](https://rollinggo.store/apply)
- [RollingGo NPX Reference](references/rollinggo-npx.md)
- [RollingGo UV Reference](references/rollinggo-uv.md)
- [Claw Host Environment Reference](references/claw-host-env.md)
- [ClawHub Skill Page](https://clawhub.ai/longcreat/skills/hotel-recommendation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and parsed JSON hotel data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RollingGo_API_KEY and a RollingGo-capable runtime; default CLI output is JSON and may include booking URLs.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
