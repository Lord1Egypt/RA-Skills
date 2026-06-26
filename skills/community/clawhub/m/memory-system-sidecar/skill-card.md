## Description: <br>
Operate, verify, rebuild, and debug the actual MemoryLab long-term memory sidecar that feeds `memory/ACTIVE_TASK_STATE.md` and `memory/LIVE_CONTEXT_PACKET.md`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sjingh](https://clawhub.ai/user/sjingh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate a repo-local MemoryLab memory sidecar, including refreshing live context from session history, rebuilding retrieval indexes, verifying tests and evals, and inspecting memory artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Refresh and rebuild commands may replace generated memory or context artifacts as part of normal operation. <br>
Mitigation: Review local generated state and context files before running refresh or rebuild commands, and back up locally modified files when needed. <br>


## Reference(s): <br>
- [Commands](references/commands.md) <br>
- [Docs Map](references/docs-map.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sjingh/memory-system-sidecar) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Markdown, Code] <br>
**Output Format:** [Markdown with inline bash commands and file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to run local refresh, verify, or rebuild scripts that update generated memory and context artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
