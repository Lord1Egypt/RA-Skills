## Description:

Automates Jianying/Xiaoyunque Seedance 2.0 video generation for text-to-video, image-to-video, and reference video-to-video workflows using a configured Jianying browser session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deemo-soul](https://clawhub.ai/user/deemo-soul)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to submit Jianying Seedance 2.0 video jobs from text prompts, reference images, or reference videos and retrieve generated MP4 outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes browser login cookies and expects a cookies.json file for Jianying authentication.

Mitigation: Remove bundled cookies before installation, revoke or rotate any exposed sessions, and provide a fresh user-controlled cookie file only in an isolated environment.

Risk: The skill can upload prompts, images, and videos to a third-party Jianying service.

Mitigation: Avoid sensitive prompts or media and run the skill with access limited to approved input and output folders.

Risk: Submitted generations can consume Jianying account credits.

Mitigation: Review duration and model settings before submission and use dry-run mode when checking form behavior.

Risk: Browser automation runs with local file access and network access to the video-generation service.

Mitigation: Run under a low-privilege account with only the required media and output directories available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deemo-soul/skills/jianying-video-gen)
- [Seedance 2.0 prompt guide](references/prompt-guide.md)
- [Jianying workspace](https://xyq.jianying.com/home)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [MP4 video files, JSON-RPC tool responses, and Markdown/plain-text command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated videos may consume Jianying account credits; dry-run mode can produce diagnostic screenshots without submitting generation.]

## Skill Version(s):

1.0.0 (source: server release metadata and MCP server_info)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
