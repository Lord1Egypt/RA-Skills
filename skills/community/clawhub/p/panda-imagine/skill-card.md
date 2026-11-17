## Description:

panda-imagine lets an agent generate images through a unified CLI across OpenAI, Azure OpenAI, Google Gemini, OpenRouter, DashScope, MiniMax, Jimeng, Seedream, and Replicate, including text-to-image, reference-image edits, aspect ratios, quality settings, and batch jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hash-panda](https://clawhub.ai/user/hash-panda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate or edit images from prompts and prompt files, route requests to an available image provider, and save generated assets to project files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation recommends installing Dreamina through a remote shell installer.

Mitigation: Avoid the `curl | bash` installer and use a verified, pinned Dreamina installation path before enabling the Jimeng CLI mode.

Risk: The skill can load API keys and provider endpoints from environment files and local project configuration.

Mitigation: Keep API keys in user-level secret storage, review provider endpoint settings before use, and avoid running the skill from untrusted repositories containing `.panda-skills/.env` or custom endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hash-panda/skills/panda-imagine)
- [Project homepage](https://github.com/hash-panda/panda-skills#panda-imagine)
- [First-time setup](references/config/first-time-setup.md)
- [Preferences schema](references/config/preferences-schema.md)
- [Dreamina CLI](https://jimeng.jianying.com/cli)

## Skill Output:

**Output Type(s):** [Files, Text, JSON, Shell commands, Configuration]

**Output Format:** [Image files with terminal path output; optional JSON status for single or batch generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated images to requested output paths, supports batch summaries, and retries retryable provider failures up to three times.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
