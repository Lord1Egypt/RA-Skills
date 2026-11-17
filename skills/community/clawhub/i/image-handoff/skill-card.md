## Description:

Detect image generation requests and route them to the artist agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[space-cadet](https://clawhub.ai/user/space-cadet)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to recognize image-generation requests, hand them off to an artist agent, and return the resulting image or response to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts, feedback, and remembered style preferences may be shared with the artist agent or retained in memory.

Mitigation: Share only the prompt and preferences needed for the current request, avoid sensitive prompt content, and review or clear stored request history when appropriate.

Risk: Automatic image-request detection can capture broad user intent and route a request after confirmation.

Mitigation: Require explicit confirmation for auto-detected requests and review the extracted prompt before handoff.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/space-cadet/skills/image-handoff)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text response with image handoff details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the original prompt, remembered style preferences, a request ID, and the artist agent result.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
