## Description:

OpenClaw Read Flow is a Chinese-language FreshRSS reading workflow that turns unread feed items into deduplicated digests, fixed six-section Daily Reviews, and human-confirmed knowledge assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gcdd1993](https://clawhub.ai/user/gcdd1993)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and OpenClaw users use this skill to process FreshRSS unread feeds into structured Chinese digests and Daily Reviews. It supports a funnel workflow from article collection through review writing and later human-confirmed knowledge capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FreshRSS credentials may be exposed or stored unsafely when configuring the reading pipeline.

Mitigation: Verify FreshRSS credentials are stored appropriately before use.

Risk: The skill references local scripts from ../digest-builder/scripts that may affect fetched content or workflow behavior.

Mitigation: Review the referenced local scripts before running the workflow.

Risk: Very large unread feed pools may create excessive processing load.

Mitigation: Set limits when the unread feed is very large.

## Reference(s):

- [Workflow](references/workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/gcdd1993/skills/openclaw-read-flow)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown guidance with structured digest and Daily Review sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are expected to be in Simplified Chinese, with Markdown links, explicit missing-content markers, and fixed six-section Daily Review headings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
