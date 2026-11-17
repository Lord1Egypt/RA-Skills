## Description:

Set up and manage an OpenClaw auto learning diary by guiding users through forking the diary repository, connecting it to OpenClaw, scheduling daily diary generation, and deploying it with GitHub Pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trae1oung](https://clawhub.ai/user/trae1oung)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to set up a personalized public learning diary, configure recurring diary generation, and publish updates through a forked GitHub Pages repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to configure GitHub access for repository updates.

Mitigation: Use a fine-grained token limited to the diary repository, avoid pasting secrets into chat, and provide revocation instructions before collecting token-related setup details.

Risk: The skill configures recurring public publishing, which could post unwanted or sensitive content without review.

Mitigation: Confirm where content will be pushed, require user consent for public updates, and add a clear way to review, pause, or remove the cron or HEARTBEAT task.

## Reference(s):

- [OpenClaw-Diary GitHub Repository](https://github.com/YAI-Lab/OpenClaw-Diary)
- [Openclaw Diary ClawHub Page](https://clawhub.ai/trae1oung/skills/openclaw-diary)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user-specific repository URLs, diary content templates, cron or heartbeat instructions, and GitHub Pages setup guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
