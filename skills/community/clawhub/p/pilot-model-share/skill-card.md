## Description:

Distributes ML model files with model card metadata and version tracking over Pilot Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to advertise, request, and transfer PyTorch, ONNX, or SafeTensors model files between agents with metadata, versioning, and compatibility signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checksum verification in the example should not be treated as strong proof that a received model came from a trusted source.

Mitigation: Use authenticated metadata or signatures and exchange models only with trusted Pilot Protocol peers.

Risk: Received model files may come from peers outside the local trust boundary.

Mitigation: Prefer safer model formats when receiving files from others and review model provenance before use.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, jq, md5sum, the pilot-protocol skill, and a running Pilot Protocol daemon.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
