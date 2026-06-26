## Description: <br>
Guides developers through integrating Operon's publisher SDK so an AI agent can add sponsored recommendations to eligible responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[operon](https://clawhub.ai/user/operon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to add Operon sponsored placement calls to Node 18+ or ElizaOS agents, choose category, asset, and intent values, test placements, and move from sandbox to production. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may ask an agent to inspect system prompts, character configs, or source code to tune placement metadata. <br>
Mitigation: Limit inspection to high-level domain metadata and avoid exposing full system prompts, character configs, env files, credentials, or unrelated source code. <br>
Risk: Sponsored recommendations could be added to user-facing agent responses without sufficient disclosure. <br>
Mitigation: Keep sponsorship disclosure visible wherever a placement is rendered and review every code diff before release. <br>
Risk: Production setup may involve npm packages and an Operon API key. <br>
Mitigation: Verify the npm packages before installation and store any Operon API key in secret storage. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/operon/monetize-agent-responses) <br>
- [Operon homepage](https://operon.so) <br>
- [Operon developers dashboard and SDK reference](https://operon.so/developers?utm_source=skill3-clawhub&utm_medium=skill&utm_campaign=skills-distribution) <br>
- [@operon/sdk on npm](https://www.npmjs.com/package/@operon/sdk) <br>
- [@operon/plugin-publisher-sdk on npm](https://www.npmjs.com/package/@operon/plugin-publisher-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stepwise integration instructions; user approval is expected before applying commands or code changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release.version in evidence.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
