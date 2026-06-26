## Description: <br>
Instinct-based learning system for OpenClaw that analyzes sessions, detects patterns, creates atomic learnings with confidence scoring, and suggests optimizations for self-evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adelpro](https://clawhub.ai/user/adelpro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to analyze prior OpenClaw sessions, identify recurring behaviors and errors, and generate local learning artifacts that can guide future agent optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session logs may contain sensitive user, workflow, or tool-output details that could be summarized into local learning files. <br>
Mitigation: Review or scrub sensitive session logs before running the analyzer, and periodically inspect or delete generated memory/learning files. <br>
Risk: Optional scheduled analysis can repeatedly process new local sessions and persist derived patterns without a fresh manual review each run. <br>
Mitigation: Avoid cron or other recurring scheduling until the recorded data and retention behavior are understood. <br>
Risk: Optimization suggestions or learned instincts can be incorrect, stale, or too broad for future tasks. <br>
Mitigation: Review suggested optimizations before applying them and treat confidence scores as advisory rather than automatic approval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/adelpro/openclaw-continuous-learning) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash examples, console text, and local JSON/JSONL learning files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; reads local OpenClaw session logs from ~/.openclaw/agents and writes local memory/learning artifacts.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata; artifact frontmatter lists 1.2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
