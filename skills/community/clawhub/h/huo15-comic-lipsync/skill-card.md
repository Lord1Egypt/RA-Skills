## Description:

Synchronizes mouth movement in video shots to dialogue audio with Kling lip-sync, and copies shots unchanged when no dialogue audio is available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and developers use this skill to process short comic or drama video shots so dialogue audio is reflected in the speaker's mouth movement. It is intended for batch lip-sync workflows that read local video and audio directories and write processed video files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads local media to external paid APIs, which can expose confidential video or audio if sensitive inputs are used.

Mitigation: Use only non-sensitive input directories unless the external provider account and data handling terms are approved for the media.

Risk: The external account can incur meaningful charges, and the built-in cost tracking should not be treated as a hard spending cap.

Mitigation: Set tight account-level budget limits with the external provider and review expected per-shot costs before batch processing.

Risk: The skill downloads generated media from external URLs after task completion.

Mitigation: Run in a controlled workspace and review downloaded outputs before using them in downstream publishing workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-comic-lipsync)
- [Kling lip-sync API endpoint](https://api.kling.com/v1/videos/lip-sync)

## Skill Output:

**Output Type(s):** [Shell commands, Files, API Calls, Guidance]

**Output Format:** [Markdown guidance with command examples; generated MP4 video files on disk]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KLING_API_KEY and local video and audio input directories.]

## Skill Version(s):

0.1.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
