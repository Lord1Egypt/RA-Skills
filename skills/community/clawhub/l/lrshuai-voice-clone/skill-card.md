## Description: <br>
Voice-cloning skill that uses a reference audio sample to generate new speech in that voice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrshu](https://clawhub.ai/user/lrshu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit prompts and reference media to supported voice-cloning models, including Kling Audio Clone and Vidu Audio Clone, and retrieve generated results from a remote API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts and media, including potentially sensitive voice samples, to a configurable remote API. <br>
Mitigation: Use only trusted TEAM_BASE_URL endpoints, confirm consent for any voice sample, and avoid private or sensitive media unless privacy and retention terms are understood. <br>
Risk: The security evidence reports unclear scope and privacy boundaries for this voice-cloning workflow. <br>
Mitigation: Review the skill before installing and document acceptable inputs, endpoint ownership, consent expectations, and data-handling controls before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lrshu/lrshuai-voice-clone) <br>
- [Default Remote API Endpoint](https://dlazy.com/api/ai/tool) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, API calls, JSON, audio generation guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TEAM_API_KEY and may send prompts and media to the configured TEAM_BASE_URL endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
