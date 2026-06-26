## Description: <br>
Tracks OpenClaw token usage and API costs from local session data, with current analysis centered on openclaw-cost-diff and a bundled Python fallback for single-window reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pfrederiksen](https://clawhub.ai/user/pfrederiksen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect local OpenClaw session history for token spend, API cost trends, model breakdowns, and window-over-window changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw session history, which can reveal usage timing, models, request volumes, and cost patterns. <br>
Mitigation: Install only where that local read access is acceptable, run with the minimum needed permissions, and treat generated JSON or dashboard exports as sensitive. <br>
Risk: The preferred workflow depends on a separately installed openclaw-cost-diff or ocost executable. <br>
Mitigation: Verify the separate executable before relying on its analysis, and use the bundled Python fallback when the diff tool is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pfrederiksen/openclaw-cost-tracker) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are derived from local OpenClaw session data and may include model, timing, token, request, and cost summaries.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
