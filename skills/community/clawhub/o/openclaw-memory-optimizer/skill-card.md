## Description: <br>
Optimizes OpenClaw 4.2 memory-search settings to improve memory retrieval accuracy, diversity, freshness, and session synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicshliu](https://clawhub.ai/user/nicshliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect and tune local OpenClaw memory-search configuration when recall, freshness, MMR diversity, or session synchronization behavior needs adjustment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent OpenClaw memory-search configuration changes may affect local agent recall, freshness, and relevance behavior. <br>
Mitigation: Back up ~/.openclaw/openclaw.json and review the exact diff or openclaw config commands before applying changes. <br>
Risk: Restarting the OpenClaw gateway can interrupt active work. <br>
Mitigation: Approve gateway restarts only when an interruption is acceptable. <br>


## Reference(s): <br>
- [OpenClaw Memory Search default parameters](references/defaults.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent local OpenClaw configuration changes for user review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
