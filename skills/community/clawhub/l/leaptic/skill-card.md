## Description: <br>
Leaptic captures every movement and highlight in front of the lens, making every moment you capture shine instantly. OpenClaw skill for Leaptic device snapshot and status access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leaptic-tech](https://clawhub.ai/user/leaptic-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure authenticated Leaptic device snapshot reads and report bound-device battery, charging state, storage, media counts, and capture timestamps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a sensitive Leaptic App-Key to read device status. <br>
Mitigation: Prefer an environment variable or secret store; if credentials are stored in ~/.config/leaptic/credentials.json, restrict file permissions. <br>
Risk: Sending the App-Key to an untrusted endpoint could expose account or device access. <br>
Mitigation: Use only official Leaptic regional Photon endpoints or a user-configured endpoint that is explicitly trusted before making requests. <br>


## Reference(s): <br>
- [Leaptic homepage](https://www.leaptic.tech/) <br>
- [ClawHub skill page](https://clawhub.ai/leaptic-tech/leaptic) <br>
- [Leaptic publisher profile](https://clawhub.ai/user/leaptic-tech) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes credential setup, regional endpoint selection, App-Key request headers, and response-field interpretation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
