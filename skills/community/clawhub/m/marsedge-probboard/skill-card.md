## Description: <br>
Query and summarize the MarsEdge probability board for BTC, ETH, SOL, and XRP 5-minute up/down signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akgod](https://clawhub.ai/user/akgod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch the live MarsEdge probability board and summarize short-horizon BTC, ETH, SOL, and XRP up/down signals with model-vs-market caveats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat probability-board summaries as financial advice. <br>
Mitigation: Present the output as market commentary, keep caveats visible, and avoid claims of certainty or trade recommendations. <br>
Risk: The skill fetches live public data from marsedge.vip, so answers can be stale or unavailable if the API is delayed or unreachable. <br>
Mitigation: Check freshness fields such as updatedAt, ts, ttl, and rem_secs before interpreting the board, and stop rather than guessing when data is unavailable. <br>
Risk: The skill may be invoked for generic crypto analysis when the user did not request MarsEdge data. <br>
Mitigation: Use it only for MarsEdge probability-board questions or when the user explicitly asks for MarsEdge data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/akgod/marsedge-probboard) <br>
- [MarsEdge live board](https://marsedge.vip) <br>
- [Edge Rules](references/edge-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Concise Markdown bullets with optional shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live board summaries are based on public MarsEdge API data and should include freshness or availability caveats when relevant.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
