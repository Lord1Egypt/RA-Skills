## Description: <br>
Fetch a token market snapshot (price/liquidity/volume) and return stable JSON (backed by Jupiter). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicholasoxford](https://clawhub.ai/user/nicholasoxford) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent builders use this skill to fetch token price, liquidity, volume, and metadata snapshots for one or more symbols, names, or mint addresses. It is intended for informational market snapshots, not wallet management, swaps, or trading recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token symbols, names, or mint addresses are sent to Vecstack for lookup. <br>
Mitigation: Submit only the token identifiers needed for the snapshot and avoid including private or unrelated information in queries. <br>
Risk: Returned market data may be incomplete, unavailable, delayed, or unsuitable as trading advice. <br>
Mitigation: Treat results as informational, preserve null fields and warnings or errors, and do not present the output as a trade recommendation. <br>


## Reference(s): <br>
- [ClawHub Market Snapshot](https://clawhub.ai/nicholasoxford/market-snapshot) <br>
- [Vecstack](https://app.vecstack.com) <br>
- [Market Snapshot API Example](https://app.vecstack.com/api/skills/market-snapshot?q=SOL&source=openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [JSON] <br>
**Output Format:** [Strict JSON object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves nulls and includes warnings or errors when market data is missing or fetches fail.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
