## Description: <br>
Establishes portfolio discipline through a mini IPS, risk budgeting, and no-margin position sizing for Vietnam equity investors; converts recommendations into conditional triggers, invalidation rules, horizon, and confidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ndtchan](https://clawhub.ai/user/ndtchan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Vietnam equity investors use this skill to turn a confirmed watchlist, holdings, risk profile, and cash-flow assumptions into a mini investment policy statement, no-margin sizing policy, per-ticker risk plan, rebalance plan, and review checklist. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat target weights, triggers, or portfolio plans as financial advice or broker orders. <br>
Mitigation: Treat outputs as planning support only, require user confirmation for target-state updates, and verify assumptions before making any investment decision. <br>
Risk: Missing holdings, weights, cash-flow, or confidence data can make position-specific sizing unsuitable. <br>
Mitigation: When required data is missing, provide a general policy, disclose assumptions, and list the exact data needed for a position-specific plan. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with five required planning sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ACTIVE_WATCHLIST and optional holdings, risk profile, and confidence inputs; assumes monthly cash inflow of 10000000 VND if missing and discloses the assumption.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
