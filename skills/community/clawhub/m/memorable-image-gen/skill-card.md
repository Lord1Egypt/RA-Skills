## Description:

Generates images with Google Gemini, scores them locally with ResMem memorability prediction, and retries with stronger composition cues until a threshold is met or the attempt limit is reached.

This skill is for research and development only.

## Publisher:

[kiwi-phantomworks](https://clawhub.ai/user/kiwi-phantomworks)

### License/Terms of Use:

MIT-0; ResMem Non-commercial License terms apply to the ResMem dependency

## Use Case:

Developers, content teams, and agents use this skill to create blog hero images, marketing visuals, social media graphics, and product thumbnails where visual recall is an explicit goal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to Google's Gemini API.

Mitigation: Avoid sending confidential or regulated prompts unless the Gemini account and data-handling terms are approved for that data.

Risk: Gemini API keys can be exposed when passed directly on the command line.

Mitigation: Use a restricted key via GEMINI_API_KEY or the local config file instead of placing keys in shell history.

Risk: The evidence identifies ResMem as non-commercial, which can affect business use.

Mitigation: Review the ResMem license terms before using this skill or its outputs in commercial contexts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kiwi-phantomworks/skills/memorable-image-gen)
- [ClawHub Metadata Homepage](https://github.com/PhantomWorksIO/clawhub-skills/tree/main/memorable-image-gen)
- [ResMem Project](https://github.com/Brain-Bridge-Lab/resmem)

## Skill Output:

**Output Type(s):** [files, shell commands, guidance]

**Output Format:** [PNG image file with terminal status text and optional memorability scores]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Gemini API key and local Python packages including resmem, torch, torchvision, pillow, and requests.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
