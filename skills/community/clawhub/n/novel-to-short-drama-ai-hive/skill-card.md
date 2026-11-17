## Description:

Helps web novel authors, rights holders, short-drama writers, and production teams turn authorized novel text into adaptation positioning, episode outlines, beat sheets, character relationships, scene boards, and first-episode storyboards, with optional AI-HIVE image and video generation commands after review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, rights holders, short-drama writers, and production teams use this skill to plan authorized novel-to-short-drama adaptations and produce reviewable script, scene, storyboard, and generation-task materials. Operators can also use the bundled scripts to create project blueprints, call AI-HIVE image or video generation APIs, and perform deterministic video edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI-HIVE API credentials and can upload private manuscripts or media.

Mitigation: Use environment or local config storage for API keys, avoid pasting real keys into prompts or logs, and upload only authorized material.

Risk: A custom base URL can redirect credentials or media to an untrusted endpoint.

Mitigation: Use the default AI-HIVE endpoint unless the alternate destination is fully trusted and reviewed.

Risk: Image and video generation commands may create billable AI-HIVE tasks.

Mitigation: Confirm prompts, routing mode, model, budget, and batch size before execution; run a small sample before batch generation.

Risk: Novel adaptation workflows can create copyright, likeness, trademark, or misleading endorsement issues.

Mitigation: Confirm rights to source text and media, keep adaptations original, and review outputs before publication or platform submission.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/novel-to-short-drama-ai-hive)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated blueprint files, model and pricing snapshots, task IDs, task status, and downloaded media paths when AI-HIVE commands are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
