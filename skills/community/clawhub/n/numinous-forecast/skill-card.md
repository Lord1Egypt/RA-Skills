## Description: <br>
Get calibrated probabilities from Numinous (Bittensor Subnet 6) with metadata/provenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Juandbalbi](https://clawhub.ai/user/Juandbalbi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users can call the Numinous forecasting API from an agent workflow to obtain probability forecasts for natural-language questions or structured events, along with returned metadata and provenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign paid x402 forecast requests using a configured crypto wallet key, and the evidence notes no artifact-level spending cap or per-call confirmation. <br>
Mitigation: Use a dedicated low-balance wallet, confirm Numinous pricing and x402 payment terms, and require an agent budget or confirmation rule before repeated calls. <br>
Risk: Forecast questions and event descriptions are sent to an external forecasting service. <br>
Mitigation: Do not submit sensitive business, personal, unreleased, or confidential questions unless the user is comfortable sending them to that service. <br>
Risk: The skill requires private wallet keys in environment variables. <br>
Mitigation: Treat wallet keys as cash, keep them out of chats and logs, and rotate them if exposure is suspected. <br>


## Reference(s): <br>
- [Numinous Labs](https://numinouslabs.io/) <br>
- [ClawHub Skill Page](https://clawhub.ai/Juandbalbi/numinous-forecast) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON forecast results and Markdown setup guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes probability, timestamp, forecaster identifier, metadata, optional parsed fields, and error state.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
