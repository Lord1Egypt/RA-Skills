## Description:

Talk face-to-face with your OpenClaw agent using a real-time video avatar powered by LiveAvatar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ennno](https://clawhub.ai/user/ennno)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to start a LiveAvatar voice and video interface that sends spoken input to an OpenClaw agent and speaks the agent response back with lip-synced video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches an unpinned npm package that executes locally while handling microphone input, a LiveAvatar API key, and local agent connectivity.

Mitigation: Use a pinned and reviewed package version, install only from a trusted publisher, and avoid running it in environments where local execution or gateway access is not acceptable.

Risk: Microphone audio, transcripts, and agent responses are part of the LiveAvatar workflow.

Mitigation: Do not speak secrets, regulated data, or sensitive business information unless LiveAvatar privacy and retention terms have been reviewed and approved for that data.

Risk: The interface depends on local OpenClaw Gateway access.

Mitigation: Run the gateway only in a trusted local environment and close the avatar session when it is no longer needed.

## Reference(s):

- [LiveAvatar](https://liveavatar.com)
- [LiveAvatar App](https://app.liveavatar.com)
- [OpenClaw](https://openclaw.ai)
- [ClawHub LiveAvatar Skill](https://clawhub.ai/ennno/skills/liveavatar)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May launch a local browser interface and requires LIVEAVATAR_API_KEY, Node.js/npm, browser microphone access, and a running OpenClaw Gateway.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
