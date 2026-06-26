## Description: <br>
Use this skill for ElevenLabs requests that read, create, update, or delete data through the OOMOL-connected ElevenLabs connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate ElevenLabs through the oo CLI with an OOMOL-connected account. It supports voice and model discovery, user and subscription lookups, history workflows, text-to-speech generation, sound effect generation, and deletion of selected history items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a connected ElevenLabs account and sensitive credentials are handled by OOMOL server-side. <br>
Mitigation: Use only an intended OOMOL account connection, avoid handling raw tokens directly, and reconnect only when an auth or connection error requires it. <br>
Risk: Write actions can generate audio or sound effects and may consume account credits or change service state. <br>
Mitigation: Inspect the live action schema first and confirm the exact payload and expected effect with the user before running write actions. <br>
Risk: The delete_history_item action permanently removes an ElevenLabs history item. <br>
Mitigation: Confirm the specific history item ID and get explicit user approval before running the destructive action. <br>


## Reference(s): <br>
- [ClawHub ElevenLabs skill page](https://clawhub.ai/oomol/oo-elevenlabs) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ElevenLabs homepage](https://elevenlabs.io) <br>
- [OOMOL oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with oo CLI shell commands and JSON request or response payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce connector transit storage references for generated or downloaded binary audio.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
