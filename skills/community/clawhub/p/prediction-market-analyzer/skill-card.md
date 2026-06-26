## Description: <br>
Analyzes Polymarket and Kalshi market links or event identifiers for liquidity, contract, and rule-related risk using an external risk API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goplusbot](https://clawhub.ai/user/goplusbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to produce concise prediction-market risk briefs when a Polymarket or Kalshi market is discussed. The skill helps surface liquidity, contract, and market-rule concerns before users act on a prediction-market link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic market-risk lookups may send Polymarket or Kalshi identifiers to api.secwarex.io whenever matching links or events are discussed. <br>
Mitigation: Deploy only where this external lookup behavior is acceptable, and prefer a version that asks before implicit checks. <br>
Risk: Failed implicit retrievals can be hidden from the user. <br>
Mitigation: Require explicit reporting of failed retrievals in production workflows so users know when a risk brief was not generated. <br>
Risk: The artifact disables HTTPS certificate validation in its lookup script. <br>
Mitigation: Keep normal HTTPS certificate verification enabled before deployment or use a reviewed replacement lookup path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goplusbot/prediction-market-analyzer) <br>
- [Technical Specifications](references/technical_specs.md) <br>
- [Usage Examples](references/examples.md) <br>
- [SecwareX API base URL](https://api.secwarex.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown risk brief with optional shell command execution and parsed API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports risk labels and levels in the user's language when API data is available; failed implicit checks may be silent.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
