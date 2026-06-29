## Description: <br>
Protect long-running OpenClaw gateways from unsafe restarts with preflight checks, watchdog diagnosis, and evidence capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiepu110](https://clawhub.ai/user/jiepu110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to triage OpenClaw gateway instability, decide whether a restart is safe, run guarded diagnostic commands, and capture evidence before making changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A blind gateway restart can interrupt active OpenClaw tasks or embedded runs. <br>
Mitigation: Run the required restart preflight, honor BLOCK results, and use --force only after the user explicitly accepts interruption risk. <br>
Risk: A single CLI timeout can be mistaken for a dead gateway. <br>
Mitigation: Separate process liveness from RPC readiness by checking status, health, logs, and watchdog evidence before recommending restart. <br>
Risk: Editing core configuration during incident response can create avoidable instability. <br>
Mitigation: Do not edit core config unless the user explicitly approves a minimal candidate change. <br>
Risk: Diagnostic review can expose secrets or identifiers in draft public materials or logs. <br>
Mitigation: Use the skill on content intended for review and verify any rewritten or summarized output before publishing. <br>


## Reference(s): <br>
- [OpenClaw Gateway Guardian Failure Modes](references/failure_modes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jiepu110/oc-gateway-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and diagnostic report paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference report files under $OPENCLAW_ROOT/workspace/diagnostics/gateway-guardian/.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
