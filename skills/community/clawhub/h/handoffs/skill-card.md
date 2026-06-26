## Description: <br>
Record and track structured task handoff logs across sessions with status, summary, artifacts, and confidence in JSONL format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sumo0221](https://clawhub.ai/user/sumo0221) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to write and read local task handoff logs so work can continue across sessions or between agents with structured status, artifacts, next steps, and confidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Handoff summaries and artifact names are saved locally under ~/.sumo/handoffs and may be displayed in terminal output. <br>
Mitigation: Avoid placing secrets, tokens, personal data, or confidential customer details in handoff text. <br>
Risk: Local handoff logs can accumulate over time and retain operational context longer than intended. <br>
Mitigation: Periodically review or delete old files in ~/.sumo/handoffs when retention matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sumo0221/handoffs) <br>
- [Publisher profile](https://clawhub.ai/user/sumo0221) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and local JSONL handoff records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and reads local handoff files under ~/.sumo/handoffs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
