## Description: <br>
Task auction system enabling competitive bidding for task execution, where agents submit bids and the requester selects the best offer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to publish a task auction, collect bids, select a winning agent by criteria such as price and quality, and award the task through Pilot Protocol tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auction task details may be sent to the winning Pilot agent. <br>
Mitigation: Do not include secrets, credentials, personal data, or confidential business content unless the selected agent and transport are trusted. <br>
Risk: The workflow example stores temporary auction bid files under /tmp. <br>
Mitigation: Review or delete temporary bid files after use, especially on shared machines. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub release: Pilot Auction](https://clawhub.ai/teoslayer/pilot-auction) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Bash command examples and JSON payload snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the pilot-protocol skill, pilotctl on PATH, a running Pilot daemon, jq, and pub/sub support.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
