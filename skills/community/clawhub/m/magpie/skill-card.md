## Description: <br>
magpie helps agents query Chinese A-share quotes, fund flows, K-lines, watchlists, alert rules, digests, and 龙虎榜 through a local daemon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[symbolstar](https://clawhub.ai/user/symbolstar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use magpie for user-requested Chinese A-share monitoring, including quotes, fund flows, K-lines, watchlists, alert rules, digests, and 龙虎榜 lookups when the local magpie daemon is already running. It is for market data monitoring, not trading, investment advice, news, or non-A-share assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can surface watchlists, alerts, alert history, and digests from a local daemon. <br>
Mitigation: Use only with a trusted local magpie daemon and treat monitoring data as private financial monitoring data. <br>
Risk: The skill can add or remove watchlist entries and alert rules. <br>
Mitigation: Review each proposed state-changing action before allowing the agent to send POST or DELETE requests. <br>
Risk: Users may interpret market monitoring output as investment advice. <br>
Mitigation: Keep responses limited to reported data and preserve the skill's instruction not to recommend trades. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/symbolstar/magpie) <br>
- [Local magpie daemon health endpoint](http://127.0.0.1:17891/api/v1/health) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with curl command examples and concise user-facing market summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted local magpie daemon at http://127.0.0.1:17891; digest responses may be forwarded as Markdown.] <br>

## Skill Version(s): <br>
0.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
