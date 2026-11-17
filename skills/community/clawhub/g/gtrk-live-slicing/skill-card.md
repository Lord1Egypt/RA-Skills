## Description:

将直播回放拆分为可编辑的逐段粗剪工程，并在生成工程前让用户确认候选切片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitruck](https://clawhub.ai/user/gitruck)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要整理直播高光的创作者和剪辑人员，用于将本地直播回放分段、生成候选切片和可编辑工程，再由用户决定选题与后续剪辑。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conflicting retry guidance could lead to another paid submission without renewed approval.

Mitigation: Before a paid resubmission, get refund confirmation or explicit approval; after a timeout, recover the existing task instead of submitting it again.

Risk: Recordings are sent for cloud processing.

Mitigation: Confirm the quoted budget and proceed only with recordings the user is comfortable sharing.

## Reference(s):

- [Gitruck CLI](https://github.com/Gitruck/cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance and shell command examples; editable video editing project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rough-cut projects and candidate clip lists for user review; no finished rendered video.]

## Skill Version(s):

1.3.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
