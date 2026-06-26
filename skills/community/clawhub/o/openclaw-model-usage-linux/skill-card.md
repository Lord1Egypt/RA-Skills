## Description: <br>
Track OpenClaw AI token usage and cost per model on Linux by parsing session JSONL files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiyouwolegequ](https://clawhub.ai/user/aiyouwolegequ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to summarize local session usage, model mix, token counts, and estimated costs across Linux OpenClaw session logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script reads local OpenClaw session logs and limited message text while inferring channels. <br>
Mitigation: Run it only on machines where local session-log access is acceptable, and review terminal output before sharing usage summaries. <br>
Risk: The script writes local usage snapshots and reset offsets for incremental comparisons. <br>
Mitigation: Back up or inspect the skill's local snapshot files if preserving prior usage state matters. <br>


## Reference(s): <br>
- [OpenClaw Model Usage (Linux) release page](https://clawhub.ai/aiyouwolegequ/openclaw-model-usage-linux) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Analysis] <br>
**Output Format:** [Plain text terminal report with token, cost, channel, model, and incremental usage summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local OpenClaw session JSONL files and updates local snapshot files for later comparisons.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
