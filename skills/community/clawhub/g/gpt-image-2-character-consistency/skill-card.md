## Description:

Guides agents to create character identity anchors and use GPT Image 2 through AI Hive to generate consistent character views, expression sheets, outfits, scenes, and sequential images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, designers, and developers use this skill to generate GPT Image 2 character reference images and scene variations while preserving identity features across poses, expressions, clothing, and multi-character storyboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AI Hive API key can be sent to a non-default API server if base URL settings are changed.

Mitigation: Keep the default API host unless the replacement endpoint is trusted; avoid untrusted --base-url, AI_HIVE_BASE_URL, or config base_url values.

Risk: The local AI Hive config file stores a sensitive API credential.

Mitigation: Treat ~/.ai-hive/config.json as a credential file, keep restrictive permissions, and use a virtual environment for dependencies.

Risk: Prompts and reference media are uploaded to the configured image-generation service.

Mitigation: Use only media and prompts that are appropriate for the configured service and avoid confidential inputs unless the service terms and controls are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/gpt-image-2-character-consistency)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, files]

**Output Format:** [Markdown guidance with bash commands and downloaded image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key and at least one reference image for the generate command.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
