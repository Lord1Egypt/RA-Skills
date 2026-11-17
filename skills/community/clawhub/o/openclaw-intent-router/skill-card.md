## Description:

Routes natural language user intents to the best matching registered agent skill using keyword, semantic, or hybrid matching with confidence scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building multi-agent systems, chatbots, voice assistants, API gateways, or workflow automation use it to map natural language requests to registered handlers with confidence thresholds and fallbacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact directs users to install mutable external npm package code and an optional global CLI that were not included in the reviewed files.

Mitigation: Review the npm package and repository source before installation, pin an exact package version, and avoid global installation unless it is necessary.

Risk: Routing a natural-language intent to a registered handler can trigger consequential downstream actions if the integrating agent exposes such handlers.

Mitigation: Require confirmation before handlers send messages, change accounts, spend money, post publicly, or modify important data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhenstaff/skills/openclaw-intent-router)
- [npm package](https://www.npmjs.com/package/openclaw-intent-router)
- [Publisher-referenced repository](https://github.com/ZhenRobotics/openclaw-intent-router)
- [Quick start documentation](https://github.com/ZhenRobotics/openclaw-intent-router/blob/main/QUICKSTART.md)
- [Examples](https://github.com/ZhenRobotics/openclaw-intent-router/tree/main/examples)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes intents locally to registered handlers and returns matched skill or capability names with confidence scores; handler behavior depends on the integrating agent.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version text)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
