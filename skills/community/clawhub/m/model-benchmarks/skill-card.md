## Description: <br>
Real-time AI model capability tracking via leaderboards (LMSYS Arena, HuggingFace, etc.) for intelligent compute routing and cost optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Notestone](https://clawhub.ai/user/Notestone) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to compare model capability and cost data, query model profiles, and generate task-specific recommendations for AI model routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release overstates live benchmark coverage while the artifact includes mock or cached benchmark behavior. <br>
Mitigation: Treat recommendations as advisory until benchmark sources, timestamps, and pricing are independently checked for the target deployment. <br>
Risk: Generated recommendations can change OpenClaw model routing and affect quality, cost, or provider selection. <br>
Mitigation: Review proposed configuration changes, keep a rollback path for existing model settings, and test recommendations on representative tasks before applying them broadly. <br>
Risk: Example automation includes cron jobs, Slack webhook alerts, and compute-router sync behavior. <br>
Mitigation: Inspect scripts before scheduling them, protect webhook URLs, and run automation first in a limited environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Notestone/model-benchmarks) <br>
- [LMSYS Chatbot Arena Leaderboard](https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard) <br>
- [LMSYS Chatbot Arena API discussions](https://huggingface.co/api/spaces/lmsys/chatbot-arena-leaderboard/discussions) <br>
- [Open LLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard) <br>
- [BigCode Leaderboard](https://huggingface.co/spaces/bigcode/bigcode-leaderboard) <br>
- [Alpaca Eval](https://tatsu-lab.github.io/alpaca_eval/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, CSV, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, JSON exports, CSV exports, Markdown examples, and configuration commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations depend on cached benchmark and pricing data in the skill artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
