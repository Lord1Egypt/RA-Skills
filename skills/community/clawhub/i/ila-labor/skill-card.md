## Description:

ILA East Coast port labor disruption signal — strike probability, inventory buffer, rerouting options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External logistics, procurement, and freight-planning agents use this skill to evaluate ILA-covered US East and Gulf Coast port labor disruption risk and decide whether to pre-position inventory, book early sailings, monitor negotiations, or proceed normally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary says this skill requires an EVM private key.

Mitigation: Use a dedicated low-balance wallet, avoid primary wallets, and set external spending limits before exposing any private key.

Risk: The server security summary says the skill can automatically trigger a higher paid tier without clearly documented limits or confirmation.

Mitigation: Confirm that the runtime validates recipient, network, token, amount, retry behavior, and paid-tier confirmation controls before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/ila-labor)
- [Signal homepage](https://datasig.ai/signals/ila-labor)
- [Example signal endpoint](https://datasig.ai/signals/ila-labor?port=USNYK)
- [Accuracy ledger](https://datasig.ai/accuracy/stats)
- [Berth congestion signal](https://datasig.ai/signals/berth-congestion)
- [Blank sailing signal](https://datasig.ai/signals/blank-sailing)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON response with a labor-risk signal, probability, confidence, contributing factors, and logistics recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes supported port codes and paid signal tiers; the higher tier can include projected disruption windows, inventory buffer days, cost of inaction, and alternative routing options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
