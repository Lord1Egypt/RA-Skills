## Description:

A coverage-controlled gate for agents. You bring your own predictor and nonconformity scores; MONARK calibrates a split-conformal region and returns commit / defer / abstain over YOUR prediction over one public MCP endpoint. Never a probability of being right, never permission to execute a tool. Four tools - attest, gate, cascade, calibrate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kraidle](https://clawhub.ai/user/kraidle)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use monark to calibrate caller-supplied nonconformity scores and gate their own predictions with commit, defer, or abstain verdicts. It helps agents audit a calibrate-to-gate loop without executing or authorizing downstream tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The public MONARK endpoint is a third-party service with no availability commitment.

Mitigation: Send only the prediction fields and calibration scores needed for gating, avoid secrets or personal data, and design callers to handle abstain, defer, and endpoint failure paths.

Risk: A gate verdict can be mistaken for permission to execute a downstream tool.

Mitigation: Treat allow as a coverage verdict on the caller's prediction only; keep execution authorization, policy checks, and human or application controls outside MONARK.

Risk: Coverage claims depend on caller-supplied nonconformity scores and exchangeability assumptions.

Mitigation: Validate the score construction and data assumptions before relying on a verdict, and abstain or recalibrate when data is shifted, time ordered, or outside the committed population.

Risk: B_t can be misunderstood as a spend cap or rate limit.

Mitigation: Use platform spend controls and rate limits for cost or throughput enforcement; treat B_t only as a caller-carried input compared with the caller's bFloor.

Risk: Operators may expose more MCP tools than needed for a deployment.

Mitigation: Use the documented include/exclude controls to expose only selected MONARK tools, such as gate and calibrate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kraidle/skills/monark)
- [MONARK MCP endpoint](https://mcp.monarkgate.tech/mcp)
- [MONARK HTTP JSON mirror](https://api.monarkgate.tech/{attest|gate|cascade|calibrate})
- [Narabi replay timeline](https://monarkgate.tech/narabi/)
- [Integration guide](INTEGRATION.md)
- [BYO walkthrough](DEMO.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with shell commands and JSON request/response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The external MCP tools return stateless JSON verdicts, quantiles, digests, and abstain reasons; the skill itself does not add local code or persistence.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
