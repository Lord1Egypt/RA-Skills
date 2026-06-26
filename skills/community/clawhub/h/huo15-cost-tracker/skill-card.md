## Description: <br>
Tracks AI API usage, token consumption, call counts, response duration, and estimated costs for configured MiniMax, OpenAI, Anthropic, and related models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jobzhao15](https://clawhub.ai/user/jobzhao15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to record LLM API token counts and durations, estimate costs from configured model pricing, review cost reports, and reset local statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local API usage metadata including token counts, model names, timestamps, durations, and estimated costs. <br>
Mitigation: Install only where this local metadata storage is acceptable and review access controls and retention for the activity stats file. <br>
Risk: A hardcoded /Users/jobzhao pricing configuration path can cause fallback pricing or inaccurate cost estimates on other machines. <br>
Mitigation: Update the pricing path or script configuration for the local environment before relying on reported costs. <br>
Risk: The reset command clears active cost statistics after writing a backup. <br>
Mitigation: Confirm the backup location and retain copies before resetting records that may be needed later. <br>


## Reference(s): <br>
- [Huo15 Cost Tracker ClawHub release](https://clawhub.ai/jobzhao15/huo15-cost-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-backed local cost reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts write local usage statistics to ~/.openclaw/workspace/memory/activity/cost-stats.json.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
