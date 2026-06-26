## Description: <br>
Track OpenClaw AI token usage and cost per model on Linux by parsing session JSONL files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HablaBechir](https://clawhub.ai/user/HablaBechir) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to summarize OpenClaw model usage, token counts, cache activity, assistant turns, and estimated cost from local Linux session logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw session JSONL files, which may contain sensitive usage or conversation metadata. <br>
Mitigation: Run it only in trusted local environments and treat generated reports as sensitive operational data. <br>
Risk: The security guidance notes that the --session flag should not be relied on for scoped reporting. <br>
Mitigation: Use --sessions-dir to point at a deliberately scoped directory, or update the skill before depending on single-session filtering. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HablaBechir/model-usage-linux) <br>
- [HablaBechir publisher profile](https://clawhub.ai/user/HablaBechir) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text usage summary or JSON report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports per-model turns, input and output tokens, cache read and write tokens, and cost in USD.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
