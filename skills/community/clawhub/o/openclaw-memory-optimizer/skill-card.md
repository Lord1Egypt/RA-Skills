## Description:

Optimizes OpenClaw 4.2 memory-search settings for retrieval quality, result count, MMR, temporal decay, and session sync thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicshliu](https://clawhub.ai/user/nicshliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review and tune OpenClaw memory-search configuration when memory retrieval is inaccurate, sparse, stale, or slow to sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent OpenClaw memory-search configuration changes can alter default agent behavior.

Mitigation: Back up ~/.openclaw/openclaw.json and review any proposed configuration diff before applying changes.

Risk: Gateway restart commands can interrupt active or shared sessions.

Mitigation: Run restart commands only during a planned maintenance window or when no active work will be disrupted.

## Reference(s):

- [OpenClaw Memory Search default parameters](references/defaults.md)
- [ClawHub skill page](https://clawhub.ai/nicshliu/skills/openclaw-memory-optimizer)
- [Publisher profile](https://clawhub.ai/user/nicshliu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent OpenClaw memory-search configuration changes and gateway restart commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
