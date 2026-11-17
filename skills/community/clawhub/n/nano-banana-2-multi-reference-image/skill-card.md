## Description:

Nano Banana 2 多参考图生成 helps agents use AI Hive's Nano Banana 2 image model to combine two or more authorized reference images with explicit roles, conflict priorities, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketing teams, and developers use this skill to generate new images from multiple authorized references while preserving assigned identity, product, structure, material, layout, palette, and style roles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloaded output filenames can be influenced by the remote service and may write outside the chosen output folder.

Mitigation: Use a dedicated output directory, review generated paths after each run, and avoid running the skill with elevated privileges.

Risk: The skill can store an AI Hive API key locally in ~/.ai-hive/config.json.

Mitigation: Use the environment variable or command-line key option when preferred, keep local key-file permissions restricted, and rotate the key if the workstation is shared or compromised.

Risk: The helper depends on the requests package at runtime.

Mitigation: Pin and review dependencies in the environment where the skill is installed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-2-multi-reference-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Files]

**Output Format:** [Markdown guidance with bash command examples and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submits AI Hive image generation tasks, reports task IDs, and downloads generated image files to a local output directory unless no-download mode is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
