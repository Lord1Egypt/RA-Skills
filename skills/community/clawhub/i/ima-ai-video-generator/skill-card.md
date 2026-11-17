## Description:

Generates short and promotional videos from text prompts or images using IMA Studio models for text-to-video, image-to-video, first-last-frame, and reference-image workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dai-shuo](https://clawhub.ai/user/dai-shuo)

### License/Terms of Use:

MIT-0

## Use Case:

Agents serving content creators, marketers, agencies, and developers use this skill to create AI-generated video clips from prompts or source images. It supports model selection, parameter guidance, image upload handling, polling, and returning a remote video URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an IMA API key and may send prompts, model parameters, and input images to IMA services.

Mitigation: Use a low-quota test key first, avoid sensitive prompts or images, and rotate keys after testing or suspected exposure.

Risk: Local model preferences and generation logs may remain under ~/.openclaw.

Mitigation: Clear ~/.openclaw/memory/ima_prefs.json and ~/.openclaw/logs/ima_skills/ when local history should not be retained.

Risk: Endpoint overrides or third-party upload examples can change where credentials or images are sent.

Mitigation: Use the default IMA endpoints, avoid custom endpoint overrides, and review or remove the ImgBB example before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dai-shuo/skills/ima-ai-video-generator)
- [IMA Studio Homepage](https://imastudio.com)
- [IMA Studio Privacy Policy](https://imastudio.com/privacy)
- [IMA API Keys](https://imastudio.com/api-keys)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Configuration, Video URL]

**Output Format:** [Markdown guidance with bash commands, JSON command output, and remote video URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IMA_API_KEY; image workflows may upload input images to IMA services and local logs/preferences may be retained under ~/.openclaw.]

## Skill Version(s):

1.0.6 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
