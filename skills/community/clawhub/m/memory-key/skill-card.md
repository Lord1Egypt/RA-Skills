## Description: <br>
Memory Key points an agent to the default OpenClaw memory folder used by the companion memory-treasure workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markma84](https://clawhub.ai/user/markma84) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to locate the OpenClaw memory folder and activate a memory workflow alongside memory-treasure. The skill provides path guidance only; memory creation, storage, and management remain outside this skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill discloses and encourages use of a local memory folder that may contain sensitive information or untrusted instructions. <br>
Mitigation: Keep secrets and untrusted instructions out of the memory folder, and review memory contents before allowing an agent to rely on them. <br>
Risk: The skill depends on the separate memory-treasure workflow for actual memory management. <br>
Mitigation: Review and install memory-treasure before using this skill as part of a complete memory workflow. <br>


## Reference(s): <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Concept memory template](artifact/examples/memory/00-概念模板.md) <br>
- [Daily memory template](artifact/examples/memory/日记录模板.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with a memory folder path and install command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Points to ~/.openclaw/workspace/memory/ and does not perform memory management.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
