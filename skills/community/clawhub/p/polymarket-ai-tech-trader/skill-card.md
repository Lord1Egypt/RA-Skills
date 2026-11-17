## Description:

Trades Polymarket prediction markets on AI model releases, tech IPOs, product launches, GPU infrastructure milestones, and AI regulation events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to operate an AI and technology themed Polymarket trading agent that discovers relevant markets, evaluates probability thresholds, and runs paper trades by default or live trades when explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket trades.

Mitigation: Use paper mode first, require deliberate live-mode activation, and do not expose a live-capable SIMMER_API_KEY to unattended automation.

Risk: Documented trading limits are not fully enforced.

Mitigation: Review or fix the volume and position-limit checks before live trading, and keep trading tunables conservative.

Risk: SIMMER_API_KEY grants trading authority.

Mitigation: Use a narrowly scoped key and keep it out of source files, shared logs, and untrusted runtime environments.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/diagnostikon/skills/polymarket-ai-tech-trader)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text status output with paper or live trading actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and configurable SIMMER_* trading parameters.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
