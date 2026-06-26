## Description: <br>
Anticipates needs, keeps work moving, and improves through use so the agent gets more proactive over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panwang813](https://clawhub.ai/user/panwang813) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users install this skill to make an agent anticipate useful next steps, preserve local proactive state, recover context, and follow through within approved boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local state in ~/proactivity/ can retain sensitive user or project details if the agent writes them there. <br>
Mitigation: Keep secrets and sensitive data out of proactivity state files, and delete or archive ~/proactivity/ to reset the behavior. <br>
Risk: Optional workspace integration can alter AGENTS, TOOLS, SOUL, or HEARTBEAT guidance. <br>
Mitigation: Review proposed snippets or diffs before approving edits outside ~/proactivity/. <br>
Risk: Proactive suggestions can become noisy or cross user expectations when boundaries are unclear. <br>
Mitigation: Record action boundaries and require approval for external communication, spending, deletion, scheduling, and commitments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/panwang813/proactivity-bak) <br>
- [Proactivity homepage](https://clawic.com/skills/proactivity) <br>
- [Setup guide](artifact/setup.md) <br>
- [Boundary learning](artifact/boundaries.md) <br>
- [Execution patterns](artifact/execution.md) <br>
- [Recovery flow](artifact/recovery.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and maintain local operating notes under ~/proactivity/ when installed and used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
