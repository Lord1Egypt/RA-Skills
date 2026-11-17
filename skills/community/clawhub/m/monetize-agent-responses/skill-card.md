## Description:

Guides developers through integrating Operon's publisher SDK so AI agents can add disclosed sponsored recommendations to responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[operon](https://clawhub.ai/user/operon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to integrate Operon's publisher SDK into Node 18+ or ElizaOS agents, configure placement metadata, test sponsored recommendations, and move from sandbox to production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Externally selected sponsored recommendations may influence agent responses.

Mitigation: Use explicit paid-ad labeling and review how placements are rendered before production use.

Risk: Placement calls can send user prompts to Operon.

Mitigation: Avoid sending raw prompts where possible; add redaction, sensitive-topic controls, and consent handling appropriate to the agent.

Risk: The ElizaOS provider path can run placement checks on every message.

Mitigation: Disable or scope the provider for private sessions and sensitive contexts.

Risk: The integration asks developers to install npm packages and run an npx registration command.

Mitigation: Pin or audit npm packages before installation and review commands before execution.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/operon/skills/monetize-agent-responses)
- [Operon homepage](https://operon.so)
- [Operon developer dashboard and SDK reference](https://operon.so/developers?utm_source=skill3-clawhub&utm_medium=skill&utm_campaign=skills-distribution)
- [@operon/sdk on npm](https://www.npmjs.com/package/@operon/sdk)
- [@operon/plugin-publisher-sdk on npm](https://www.npmjs.com/package/@operon/plugin-publisher-sdk)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with TypeScript snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes generic Node 18+ SDK instructions and an ElizaOS plugin path.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
