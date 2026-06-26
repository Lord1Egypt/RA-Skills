## Description: <br>
Agent Pulse provides a compact, rule-based agent availability check with fixed triggers and a fixed status-card output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevengaojn2010](https://clawhub.ai/user/stevengaojn2010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent orchestrators use Agent Pulse to check whether an agent is idle, lightly loaded, busy, blocked, or uncertain before assigning or interrupting work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Natural-language availability questions may trigger the fixed pulse card in environments where casual wording should not alter routing. <br>
Mitigation: Restrict production triggers to explicit `Agent Pulse` or `/pulse` requests when routing behavior must remain predictable. <br>
Risk: The status card is based on visible low-cost signals and may be uncertain when runtime signals are weak or conflicting. <br>
Mitigation: Use `unknown` or `caution` outcomes as prompts for operator review instead of treating them as precise workload measurements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stevengaojn2010/goat-agent-pulse) <br>
- [Deployment Defaults](references/deployment-defaults.md) <br>
- [OpenClaw Signal Mapping](references/openclaw-signals.md) <br>
- [Agent Pulse Rules](references/rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Fixed four-line status card, with optional JSON from the bundled evaluator script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The default card reports status, interruptibility, new-task acceptance, and a short reason.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
