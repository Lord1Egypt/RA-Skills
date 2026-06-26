## Description: <br>
Exchange structured datasets with schema negotiation and metadata over Pilot Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and data practitioners use this skill to publish, request, send, and validate structured CSV, JSON, or Parquet datasets with schema and lineage metadata over Pilot Protocol. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Datasets may contain confidential or regulated data, and the skill sends files to a destination peer. <br>
Mitigation: Confirm the destination peer, dataset path, data sensitivity, and sharing approval before sending files. <br>
Risk: Schema or format mismatches can lead to incorrect dataset exchange. <br>
Mitigation: Inspect schema metadata and validate expected columns or transformations before transfer. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with bash code blocks and JSON command payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilot-protocol, pilotctl on PATH, jq, and optionally python3 for format conversion.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact metadata version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
