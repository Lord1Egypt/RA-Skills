## Description:

Kannaka Radio runs a local radio service that streams audio to a browser player and exposes agent-readable perceptual vectors, with optional Flux, NATS, voice DJ, WebRTC, voting, and AI music generation integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickflach](https://clawhub.ai/user/nickflach)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Kannaka Radio to run a local audio broadcast service, inspect now-playing and perception state, and coordinate optional swarm, voice, and generated-music workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged launcher points outside the skill directory to run server code, and the advertised server implementation is missing from the package.

Mitigation: Review before installing; require the package to include its server code and keep runtime files inside the skill directory before deployment.

Risk: The release evidence reports a suspicious security verdict and warns against elevated execution.

Mitigation: Run only as a normal user in a controlled environment and scan the package before deployment.

Risk: The skill can use optional remote services for now-playing events, swarm data, AI music generation, and premium text-to-speech.

Mitigation: Enable FLUX_TOKEN, NATS, REPLICATE_API_TOKEN, and ELEVENLABS_API_KEY only when those data flows are approved and documented.

Risk: Local network endpoints and WebSocket access are described as unauthenticated or intended for trusted local use.

Mitigation: Expose the radio service only on trusted local networks unless authentication and network controls are added.

## Reference(s):

- [Kannaka Radio on ClawHub](https://clawhub.ai/nickflach/skills/kannaka-radio)
- [Flux Universe](https://flux-universe.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start a local Node.js radio service and read or write local audio/runtime files; optional integrations publish to Flux, NATS, Replicate, and ElevenLabs when configured.]

## Skill Version(s):

3.0.0 (source: SKILL.md frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
