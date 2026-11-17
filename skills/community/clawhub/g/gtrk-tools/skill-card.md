## Description:

Guides an agent in selecting and operating gtrk single-purpose tools for media editing, conversion, and analysis, then reporting the resulting files, task status, and costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitruck](https://clawhub.ai/user/gitruck)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to select gtrk tools for image, video, and audio workflows. The agent handles CLI invocation and explains outputs, costs, and recovery steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media sent to cloud services may contain content the user does not want uploaded.

Mitigation: Use only media the user is comfortable sending to cloud services.

Risk: Cloud tool usage may incur charges.

Mitigation: Check the quoted charges before running a tool.

Risk: Voice cloning may be used without a speaker's consent.

Mitigation: Obtain consent before cloning someone's voice.

Risk: Rerunning exports can affect editing drafts, and restarting interrupted tasks can cause duplicate billing.

Mitigation: Back up editing drafts before rerunning exports and recover existing task IDs after interruptions.

## Reference(s):

- [gtrk CLI documentation](https://github.com/Gitruck/cli)
- [gtrk CLI usage tutorial](https://hocassian.feishu.cn/wiki/HCFpwoF7SivIFbkKosgcFMcEnxk)
- [ClawHub skill page](https://clawhub.ai/gitruck/skills/gtrk-tools)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Media files]

**Output Format:** [Markdown guidance with shell commands and structured task results; gtrk tools may produce media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool-dependent outputs include edited or converted media, structured analysis results, subtitles, and MIDI files.]

## Skill Version(s):

1.3.10 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
