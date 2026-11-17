## Description:

This skill helps agents prepare AI Hive Seedance 2.5 commands for silent presenter visuals, B-roll, demo inserts, background edits, and outro holds for HeyGen-style explainer video workflows while excluding voice cloning, avatar binding, lip-sync, TTS, and subtitle generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketing teams, and developers use this skill to plan and invoke AI Hive video-generation tasks for silent visual assets in corporate training, product demos, and avatar-adjacent explainer videos. Narration, subtitles, voice, and lip-sync remain separate authorized post-production workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images, videos, and prompts may be sent to AI Hive.

Mitigation: Avoid sensitive source media, confirm rights and consent for presenter or product assets, and use the skill only when the AI Hive transfer is acceptable.

Risk: The helper stores an AI Hive API key locally when using the auth command.

Mitigation: Prefer a virtual environment or controlled user account, restrict file permissions, and rotate the key if the local environment is shared or compromised.

Risk: Downloaded outputs depend on server-provided result URLs and task identifiers.

Mitigation: Use a controlled output directory and review or patch URL validation and taskId filename handling before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/heygen-video-generation-alternative)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script can submit AI Hive video-generation tasks, upload selected local image or video inputs, and save generated MP4 results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
