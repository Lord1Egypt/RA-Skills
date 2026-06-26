## Description: <br>
Read-only access to the GM3 Alertworthy feed, providing real-time token market data for analysis agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigbadman-lab](https://clawhub.ai/user/bigbadman-lab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysis agents use this skill to access the GM3 Alertworthy feed and inspect token market snapshots for downstream analysis. The skill provides read-only market data context and does not perform filtering, ranking, or trading actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a GM3 Developer API key to call the documented feed. <br>
Mitigation: Store the key as a secret and avoid logging Authorization headers or exposing the key in client-side code. <br>
Risk: Returned market data could be mistaken for trading instructions. <br>
Mitigation: Treat the feed as analysis input only; keep strategy logic, filtering, decisions, and any execution outside this skill. <br>


## Reference(s): <br>
- [GM3 Alertworthy feed endpoint](https://api.gm3.fun/functions/v1/gm3-api/v1/paid/alertworthy) <br>
- [ClawHub skill page](https://clawhub.ai/bigbadman-lab/gm3-alertworthy-feed) <br>
- [Publisher profile](https://clawhub.ai/user/bigbadman-lab) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API call, JSON data] <br>
**Output Format:** [Markdown guidance describing a read-only GET request and JSON response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GM3 Developer API key; the endpoint accepts no input parameters.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
