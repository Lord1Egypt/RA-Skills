## Description:

Guides an agent through preparing talking-head footage, aligning a separate voice recording when present, and creating editable oral-cut projects with gtrk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitruck](https://clawhub.ai/user/gitruck)

### License/Terms of Use:

MIT-0

## Use Case:

External video editors use this skill to turn talking-head footage into editable projects by aligning a separate voice recording when present and trimming filler, retakes, and long pauses. It guides the agent to deliver gtrk, Jianying, and Premiere XML projects, with optional local rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud processing may send media and transcripts to Gitruck and incur charges.

Mitigation: Use only media and transcripts suitable for sending to Gitruck's cloud, and check the current estimate with --dry-run before processing.

Risk: Installing downloaded media tools introduces a software integrity risk.

Mitigation: Verify downloaded tools against trusted upstream checksums before installation.

## Reference(s):

- [Gitruck CLI homepage](https://github.com/Gitruck/cli)
- [ClawHub skill release](https://clawhub.ai/gitruck/skills/gtrk-oralcut)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance and gtrk, Jianying, and Premiere XML project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also produce an MP4 through optional local rendering.]

## Skill Version(s):

1.3.10 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
