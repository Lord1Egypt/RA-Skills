## Description:

Generate expressive talking-head videos from static images using Kameo AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veya2ztn](https://clawhub.ai/user/veya2ztn)

### License/Terms of Use:

MIT

## Use Case:

Developers, creators, and agents use this skill to turn portraits or avatars into short talking-head videos from a prompt or dialogue. It supports basic Kameo generation, optional Gemini-assisted prompt enhancement, credit checks, and account/API-key setup guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation includes a concrete-looking Kameo API key value that should be treated as exposed.

Mitigation: Use a newly generated personal Kameo API key, rotate any copied key, and avoid committing credentials to documentation or config examples.

Risk: The registration helper accepts passwords on the command line and prints/saves sensitive credential material.

Mitigation: Avoid the helper as written; register through a trusted account flow and keep credentials out of shell history, logs, and shared terminals.

Risk: The enhanced prompt helper interpolates image paths and dialogue into a shell heredoc before Python execution.

Mitigation: Do not run it on untrusted filenames or dialogue until quoting and input passing are fixed.

Risk: Video generation uploads portraits, prompts, and optional Gemini prompt-enhancement inputs to external services.

Mitigation: Upload only images and dialogue you have permission to process and that are acceptable to send to Kameo and Google Gemini.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/veya2ztn/skills/kameo)
- [Kameo homepage](https://kameo.chat)
- [Kameo public API base](https://api.kameo.chat/api/public)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands plus generated MP4/video URL output from Kameo.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KAMEO_API_KEY; the enhanced workflow also requires GOOGLE_API_KEY and sends images and prompts to external services.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
