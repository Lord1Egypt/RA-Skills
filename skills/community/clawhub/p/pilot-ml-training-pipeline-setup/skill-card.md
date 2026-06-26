## Description: <br>
Deploys an end-to-end ML training pipeline across data preparation, training, evaluation, and serving agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML infrastructure teams use this skill to configure a four-agent Pilot pipeline for data preparation, training, evaluation, and model serving. It helps coordinate role-specific skill installation, hostnames, peer handshakes, and pipeline manifests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trust links and model or dataset transfers can expose sensitive assets if peers are misidentified. <br>
Mitigation: Confirm each Pilot hostname belongs to the intended node, handshake only with known peers, and apply required approvals before transferring sensitive datasets or model checkpoints. <br>
Risk: Role setup may replace an existing ML training pipeline manifest. <br>
Mitigation: Check or back up ~/.pilot/setups/ml-training-pipeline.json before applying generated setup steps. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-ml-training-pipeline-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces role-specific setup instructions and manifest templates; does not execute commands by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
