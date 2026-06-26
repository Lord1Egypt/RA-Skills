## Description: <br>
Persistent NDJSON event logging with rotation, compression, and retention policies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to persist Pilot Protocol event streams, audit event history by timestamp or topic, and export retained events for external analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent event logs may capture secrets or personal data, especially when using broad source or topic subscriptions. <br>
Mitigation: Configure narrow sources and topics where possible, avoid logging secrets or personal data, and review export practices before use. <br>
Risk: Durable logs under /var/log/pilot-events can create retention and access-control exposure. <br>
Mitigation: Restrict permissions on /var/log/pilot-events and align rotation, compression, and deletion schedules with organizational retention requirements. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-event-log) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples and workflow snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Assumes pilotctl, jq, gzip, and a running Pilot daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
