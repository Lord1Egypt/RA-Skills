## Description: <br>
Isolate suspicious agents pending investigation in Pilot Protocol networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and incident responders use this skill to temporarily isolate suspicious Pilot Protocol agents, review quarantine records, and release agents after investigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Quarantine examples can disconnect live agents even though immediate disconnects are described as out of scope. <br>
Mitigation: Require manual operator review before running disconnect commands, and separate temporary trust suspension from session termination when adapting the workflow. <br>
Risk: Active containment commands can disrupt legitimate Pilot Protocol sessions if the target agent is misidentified. <br>
Mitigation: Confirm the agent identity and investigation reason before applying untrust or disconnect operations. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot Quarantine on ClawHub](https://clawhub.ai/teoslayer/pilot-quarantine) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash command blocks and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, jq, openssl, and a running Pilot Protocol daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
