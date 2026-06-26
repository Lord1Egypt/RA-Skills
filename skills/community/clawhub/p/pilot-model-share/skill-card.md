## Description: <br>
Distribute ML model files with model card metadata and version tracking over Pilot Protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to announce, request, and transfer PyTorch, ONNX, or SafeTensors model files with model metadata and version information over Pilot Protocol. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Model files can expose proprietary weights, metadata, license terms, or compliance-sensitive content if sent to the wrong recipient or shared without authorization. <br>
Mitigation: Confirm the destination peer and authorization to disclose the model before sending any model file or metadata. <br>
Risk: The artifact's example validates transfers with an MD5 checksum, which is weak for important integrity checks. <br>
Mitigation: Use SHA-256 checksums or signed metadata for important model transfers. <br>
Risk: The skill depends on pilotctl and a running Pilot Protocol daemon. <br>
Mitigation: Install pilotctl from a trusted source and verify the daemon is running before using the commands. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-model-share) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON command payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, jq, md5sum, the pilot-protocol skill, and a running Pilot Protocol daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
