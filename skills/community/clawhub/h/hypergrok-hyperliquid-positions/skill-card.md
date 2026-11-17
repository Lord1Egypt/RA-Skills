## Description:

Manage Hyperliquid perp positions and margin from the desk computer - read positions and margin, set leverage and cross/isolated mode, add isolated margin, understand margin tiers and liquidation price, close a position with a reduce-only IOC, and clean up orphaned orders. Write actions are Execution Trader only, on an approved or mandate-covered ticket. Use for leverage changes, closes, protection checks and margin questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Risk Managers use the read guidance to review Hyperliquid perpetual positions, margin, liquidation distance, and protective orders. Execution Traders use the write guidance for leverage, margin, and close actions only against an approved or mandate-covered ticket.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Leverage, margin, and close actions can change exposure and liquidation risk.

Mitigation: Restrict write actions to an Execution Trader acting on an approved or mandate-covered ticket; check live position size immediately before a close and confirm the resulting position and orders afterward.

Risk: The skill makes external Hyperliquid API requests, and the scanner review was incomplete with medium confidence.

Mitigation: Review the unresolved local references and confirm the intended Hyperliquid network before use; treat the scanner's benign verdict as limited assurance.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, API calls, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes read and execution guidance for Hyperliquid positions and margin.]

## Skill Version(s):

1.9.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
