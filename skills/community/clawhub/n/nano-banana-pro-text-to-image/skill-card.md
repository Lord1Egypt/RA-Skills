## Description:

Nano Banana Pro 文生图 helps agents turn text prompts into polished commercial and creative images through AI Hive, with guidance for subject, space, lighting, color, material, lens, composition, and negative constraints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and brand teams use this skill to create text-only Nano Banana Pro image-generation workflows for portraits, product stills, architecture concepts, fashion editorials, and campaign series. The skill provides prompt guidance plus CLI commands for submitting AI Hive image tasks, checking task status, and downloading generated outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloaded result URLs and generated filenames are not safely constrained.

Mitigation: Run with a dedicated output directory, avoid privileged working contexts, and prefer a hardened version that validates download hosts and keeps saved files inside the selected output folder.

Risk: The skill stores and uses an AI Hive API key locally.

Mitigation: Install only if AI Hive is trusted, keep the local config at 0600 permissions or use AI_HIVE_API_KEY, and rotate the key if exposure is suspected.

Risk: Synthetic images involving real people or news-like scenes could be mistaken for documentary evidence.

Mitigation: Do not present generated images as factual records, and label outputs clearly when they depict real identities or current events.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-pro-text-to-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands; CLI execution may return JSON task data and downloaded image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved to a selected output directory; AI Hive API keys may be read from the command line, AI_HIVE_API_KEY, or a local 0600 config file.]

## Skill Version(s):

1.0.1 (source: server release evidence and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
