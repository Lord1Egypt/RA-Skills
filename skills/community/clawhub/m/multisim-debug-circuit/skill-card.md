## Description:

诊断并以最小、可回滚修改修复 Multisim 电路或仿真故障；use for invalid netlists, convergence failures, wrong waveforms, bias errors, or missing outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxy050208](https://clawhub.ai/user/yxy050208)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to debug Multisim circuit simulations by separating runtime environment failures from circuit defects, inspecting bounded evidence, proposing minimal reversible DesignPatch changes, and comparing retest results before declaring a fix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may inspect circuit-related logs, netlists, commands, reports, and experiment directories.

Mitigation: Install and use the skill only when the Multisim MCP workflow is intended and those circuit artifacts are appropriate for agent review.

Risk: A proposed DesignPatch could modify the original project if persisted without review.

Mitigation: Review the proposed change, rollback method, and retest evidence before giving separate approval to persist changes.

Risk: A circuit issue could be incorrectly treated as fixed without enough retest evidence.

Mitigation: Require comparison of original and candidate retest results, and keep the status as failed or unverified when evidence is missing.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown structured as symptoms, evidence, root cause, minimal change, retest result, and residual risk.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed DesignPatch details and retest comparison notes; persistence requires separate user approval.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
