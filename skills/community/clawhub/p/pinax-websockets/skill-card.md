## Description: <br>
Connects agents to a substreams-websocket fan-out server for real-time blockchain table data over WebSocket, with selectors, SQE filters, reconnect handling, chain reorg handling, and backpressure guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pinax](https://clawhub.ai/user/pinax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to connect to live Substreams DatabaseChanges feeds, subscribe to network and table streams, filter events, and handle live-feed operational cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted or misconfigured WebSocket servers can expose subscriptions or deliver unreliable blockchain data. <br>
Mitigation: Connect only to trusted operators and confirm advertised streams through the session message or /streams before relying on data. <br>
Risk: The feed is live-only and may drop frames or report chain reorganizations. <br>
Mitigation: Handle dropped and undo lifecycle frames, reconnect with backoff, and backfill gaps from Substreams or another authoritative source. <br>
Risk: Broad wildcard subscriptions or weak filters can overwhelm clients or increase irrelevant data exposure. <br>
Mitigation: Scope selectors and SQE filters to required networks, tables, and fields, and monitor backpressure or HTTP 503 responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pinax/pinax-websockets) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, code] <br>
**Output Format:** [Markdown with WebSocket URL examples and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; consumers must provide and trust the WebSocket endpoint they connect to.] <br>

## Skill Version(s): <br>
0.6.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
