## Description:

MiniMax Coding Plan provides MiniMax-native web search and image understanding for OpenClaw when an agent needs MiniMax search or vision capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjli-new](https://clawhub.ai/user/yjli-new)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to route explicit MiniMax web search requests and MiniMax image analysis requests through a local OpenClaw wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper can send credential-bearing requests and uploaded image content to the configured MiniMax endpoint.

Mitigation: Install only when the MiniMax endpoint configuration and invoking agents are trusted, and avoid sending sensitive local screenshots or private-network image URLs.

Risk: An untrusted MINIMAX_API_HOST value could redirect requests away from the intended MiniMax service.

Mitigation: Use a trusted MiniMax API host configuration before invoking web search or image understanding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yjli-new/skills/minimax-coding-plan)
- [MiniMax API endpoint](https://api.minimaxi.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses, with optional plain text content for image analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MiniMax API credentials or a configured minimax-portal OAuth profile.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
