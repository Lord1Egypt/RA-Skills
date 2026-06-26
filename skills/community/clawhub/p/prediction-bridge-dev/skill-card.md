## Description: <br>
Search Prediction Bridge prediction-market events by text or X (Twitter) link via the backend API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallyunet](https://clawhub.ai/user/smallyunet) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to find Prediction Bridge prediction-market events that match a topic, article URL, or X link, then present ranked event links with concise market snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user search text, article URLs, or X links to the Prediction Bridge backend. <br>
Mitigation: Use it only for non-confidential inputs and avoid secrets, private documents, or private links. <br>
Risk: The PREDICTION_BRIDGE_API_URL override can redirect requests to a different service. <br>
Mitigation: Set PREDICTION_BRIDGE_API_URL only to a Prediction Bridge endpoint or another service the operator explicitly trusts. <br>


## Reference(s): <br>
- [Prediction Bridge homepage](https://www.predictionbridge.xyz) <br>
- [ClawHub skill page](https://clawhub.ai/smallyunet/prediction-bridge-dev) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown summary derived from JSON API responses, with shell commands for API calls when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ranks matched events by relevance score and presents concise event links, source names, scores, and market snapshots.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
