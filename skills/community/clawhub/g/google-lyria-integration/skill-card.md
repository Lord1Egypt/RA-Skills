## Description:

Generate 30-second instrumental music via Google Lyria (Vertex AI). Use when user requests music generation, specific styles/keys/instruments, or music iteration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[menopeter](https://clawhub.ai/user/menopeter)

### License/Terms of Use:


## Use Case:

Developers, creators, and agents use this skill to configure Google Cloud access, craft music prompts, call Google Lyria through Vertex AI, and save short instrumental WAV tracks for social video, transitions, loops, or iteration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Google access tokens may be stored in plaintext workspace configuration.

Mitigation: Avoid storing live tokens when possible, restrict credential file permissions, and refresh tokens through gcloud when needed.

Risk: Prompts and billable generation requests are sent to Google Vertex AI.

Mitigation: Confirm the configured Google Cloud project and region before generating music, and review prompts for sensitive or unintended content.

Risk: The documented setup flow includes installing gcloud before use.

Mitigation: Use official Google Cloud SDK installation instructions and review install commands before running them.

## Reference(s):

- [Google AI music generation documentation](https://ai.google.dev/gemini-api/docs/music-generation)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and generated WAV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated audio is limited to 30-second instrumental WAV files with custom or timestamped filenames.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
