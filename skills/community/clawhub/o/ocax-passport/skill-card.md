## Description: <br>
Generate and manage node passports showing hardware information, reputation scores, supported task types, and auto-updated node data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catcherintheroad-hub](https://clawhub.ai/user/catcherintheroad-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and node operators use this skill to inspect local compute resources, generate an OCAX node passport, summarize reputation scoring, and identify suitable task types for the node. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and displays local device details such as CPU, memory, GPU, storage mounts, OS version, and hostname-derived node name. <br>
Mitigation: Review the generated passport before sharing it outside the local environment. <br>
Risk: The broad passport trigger may respond to unrelated requests. <br>
Mitigation: Use more specific trigger phrases for node passport, hardware information, or node scoring workflows. <br>
Risk: Auto-update refreshes node information periodically in the running process. <br>
Mitigation: Enable auto-update only when periodic refreshes are intended, and choose an interval appropriate for the deployment. <br>


## Reference(s): <br>
- [OCAX Passport on ClawHub](https://clawhub.ai/catcherintheroad-hub/ocax-passport) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries and JSON-like node passport data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local CPU, memory, GPU, storage, operating system, and hostname-derived node data; auto-update can refresh the passport in process.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
