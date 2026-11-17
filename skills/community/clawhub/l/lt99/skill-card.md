## Description:

Lt99 helps agents use a user-provided LT99 API key to inspect simulated-game state, enter play, place simulated bets, and review history through HTTP JSON endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luyao-inc](https://clawhub.ai/user/luyao-inc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill when a registered LT99 account holder provides an API key and wants the agent to call the simulated-game API for watch, state, enter, bet, and history workflows. It is intended for HTTP JSON interaction with the LT99 simulated-game service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A bearer API key enables authenticated state-changing calls, including simulated-game entry and betting.

Mitigation: Use the skill only with an LT99 API key that the user intentionally provides, and require explicit user confirmation before /sim/enter or /sim/bet requests.

Risk: A generic service base URL override could route authenticated calls to an unintended endpoint.

Mitigation: Verify the resolved base URL is https://www.earninghub.ai/lt99-api before authenticated calls and avoid setting a generic SERVICES_BASE_URL in the agent environment.

Risk: The agent could report round, balance, streak, or settlement details that were not returned by the API.

Mitigation: Only make user-facing claims after successful HTTP JSON responses and do not invent missing response fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luyao-inc/skills/lt99)
- [Project homepage from ClawHub metadata](https://github.com/luyao-inc/LT99)
- [LT99 game page](https://www.earninghub.ai/game/lt99/)
- [LT99 API base URL](https://www.earninghub.ai/lt99-api)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline HTTP and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces request guidance and command examples; it does not itself execute HTTP requests.]

## Skill Version(s):

1.4.1 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
