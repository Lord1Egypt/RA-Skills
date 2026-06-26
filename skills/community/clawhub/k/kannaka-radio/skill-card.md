## Description: <br>
Kannaka Radio runs a local browser radio service that streams audio for humans, exposes playback and perception data for agents, and optionally integrates Flux, NATS, Replicate, and TTS providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NickFlach](https://clawhub.ai/user/NickFlach) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Kannaka Radio to run a local music radio service, inspect playback and perception state, coordinate listener or swarm features, and manage audio workflows through shell commands and HTTP endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The launcher may run server code outside the reviewed skill package. <br>
Mitigation: Confirm the intended server code and package files are present before installing or running the skill. <br>
Risk: Flux, WebRTC, and live-broadcast features can publish audio or metadata when enabled. <br>
Mitigation: Keep those features disabled unless publication is intended, and use environment-specific provider tokens. <br>
Risk: The documentation mentions a built-in Flux token fallback for remote publishing. <br>
Mitigation: Set and manage your own FLUX_TOKEN for any intended Flux use and review the publication destination before enabling it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/NickFlach/kannaka-radio) <br>
- [Publisher profile](https://clawhub.ai/user/NickFlach) <br>
- [Flux Universe](https://flux-universe.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON API/WebSocket examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can start or control a local radio server, return playback and perception JSON, and write local audio, voice, and generated-music files when enabled.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
