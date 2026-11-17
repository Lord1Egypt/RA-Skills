## Description:

Generates podcast-style audio narratives from text using Azure OpenAI GPT Realtime Mini over WebSocket, with React, FastAPI, streaming, and PCM-to-WAV implementation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thegovind](https://clawhub.ai/user/thegovind)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add podcast-style text-to-speech generation to applications with Azure OpenAI Realtime API, including backend audio synthesis, frontend playback, and PCM-to-WAV conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Azure OpenAI API keys may be exposed or misused if copied into client-side code, logs, or shared artifacts.

Mitigation: Store API keys only in server-side secret management, avoid logging secret values, and rotate keys if exposure is suspected.

Risk: Generated content is sent to a cloud provider and may be subject to provider and application retention policies.

Mitigation: Confirm provider and application retention rules before use, and avoid sending confidential, regulated, customer, or otherwise sensitive content unless approved.

Risk: Connecting to an unexpected endpoint can route content or credentials to the wrong service.

Mitigation: Validate or allowlist the Azure OpenAI endpoint before opening the WebSocket connection.

Risk: The helper CLI can overwrite files when deriving a WAV path from a supplied PCM filename.

Mitigation: Pass only expected .pcm inputs or change the helper to require an explicit output path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thegovind/skills/podcast-generation)
- [Architecture Reference](references/architecture.md)
- [Code Examples](references/code-examples.md)
- [Podcast Generation Acceptance Criteria](references/acceptance-criteria.md)
- [PCM to WAV helper](scripts/pcm_to_wav.py)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python, JavaScript, shell, and environment-variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation guidance for Azure OpenAI Realtime WebSocket audio generation, transcript handling, and WAV playback.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
