## Description:

Memory Key points an agent to the default memory folder used by the memory palace workflow and relies on the companion memory-treasure skill for actual memory management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markma84](https://clawhub.ai/user/markma84)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to locate and activate personal memory files stored under the default memory palace path. It is intended to work alongside memory-treasure, which handles memory management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may assume this skill manages memory directly.

Mitigation: Confirm the companion memory-treasure skill is installed and trusted before using Memory Key for a memory workflow.

Risk: The workflow points agents to files under ~/.openclaw/workspace/memory/, which may contain personal or sensitive memory content.

Mitigation: Review the memory folder contents and access expectations before enabling the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/markma84/skills/memory-key)
- [Publisher profile](https://clawhub.ai/user/markma84)
- [Memory concept template](artifact/examples/memory/00-概念模板.md)
- [Daily memory template](artifact/examples/memory/日记录模板.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with memory file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the default memory path ~/.openclaw/workspace/memory/ and depends on memory-treasure for memory management.]

## Skill Version(s):

2.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
