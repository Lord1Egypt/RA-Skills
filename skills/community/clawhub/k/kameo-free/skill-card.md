## Description:

Generate expressive talking-head videos from static images using Kameo AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veya2ztn](https://clawhub.ai/user/veya2ztn)

### License/Terms of Use:

MIT

## Use Case:

Developers and creators use this skill to generate short talking-head videos from portraits or avatars, optionally enhancing prompts with vision analysis for more expressive facial motion and lip-sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded API credentials and plaintext local credential storage can expose secrets.

Mitigation: Remove and rotate embedded keys before release, require users to provide their own credentials, and prefer environment variables or a secret manager over checked-in examples or plaintext config files.

Risk: Passing passwords as command-line arguments can expose them through shell history or process listings.

Mitigation: Collect passwords through a protected prompt or external secret store instead of positional command-line arguments.

Risk: The enhanced prompt script can turn untrusted image paths or dialogue into local code execution through heredoc interpolation.

Mitigation: Do not run the enhanced prompt workflow on untrusted inputs until the script safely passes values as arguments or environment variables and quotes all data boundaries.

Risk: Portrait images and prompts are uploaded to Kameo, and enhanced generation also uploads image data to Google Gemini.

Mitigation: Use only content that users are authorized to upload and disclose the third-party processing path before generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/veya2ztn/skills/kameo-free)
- [Kameo homepage](https://kameo.chat)
- [Kameo public API](https://api.kameo.chat/api/public)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown, Files]

**Output Format:** [Markdown guidance with shell commands and generated video file or media URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Kameo API credentials; enhanced generation also uses a Google API key and uploads images to third-party services.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
