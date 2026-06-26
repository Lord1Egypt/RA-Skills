## Description: <br>
Provides predefined constrained tool subsets for spawning sub-agents tailored to task types like Explore, Plan, Verification, Coding, and Secretary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanxiao-bot](https://clawhub.ai/user/hanxiao-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to choose prompt-level tool subsets when delegating Explore, Plan, Verification, Coding, or Secretary tasks to sub-agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt-level tool subsets are soft constraints and may not enforce actual platform permissions. <br>
Mitigation: Use platform/tooling controls to enforce execution, file-edit, and network permissions before using the subsets for sensitive work. <br>
Risk: The Secretary subset documentation contains an internal contradiction about search tools. <br>
Mitigation: Review and resolve the Secretary search-tool permissions before relying on that subset. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hanxiao-bot/openclaw-subagent-toolset) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with prompt snippets and tool-subset lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Soft prompt-level constraints; platform-level tool permissions remain external.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
