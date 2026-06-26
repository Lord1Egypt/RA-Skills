## Description: <br>
Real-time NDJSON data streaming over persistent Pilot Protocol connections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to stream structured NDJSON data, such as sensor readings, logs, or metrics, between agents over persistent Pilot Protocol connections with backpressure handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Streaming to an unintended destination can expose data or send traffic to the wrong Pilot Protocol peer. <br>
Mitigation: Set DEST intentionally before running examples and verify the target connection before starting a stream. <br>
Risk: Continuous stream loops and background listeners can run longer than intended. <br>
Mitigation: Add a stop condition, supervise background processes, and stop listeners when the workflow is complete. <br>
Risk: Stream logs may contain private data or credentials. <br>
Mitigation: Avoid streaming sensitive values and delete or protect /tmp/pilot-stream.log when it may contain sensitive data. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-stream-data) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command examples for streaming, receiving, subscribing, and processing NDJSON data with pilotctl.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
