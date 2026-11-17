## Description:

Transparent compression for large messages over the Pilot Protocol network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to compress large text, JSON, binary, or bulk payloads before sending them over Pilot Protocol, then decompress received payloads after retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The send and receive examples are network-facing and can transmit data to named Pilot Protocol peers.

Mitigation: Verify the recipient and transport before sending, and avoid sending secrets or personal data unless the recipient and channel are trusted.

Risk: Decompressing received content can expand data unexpectedly or process content from an untrusted sender.

Mitigation: Verify the sender, use size limits, and decompress received content only in a private working directory.

## Reference(s):

- [Pilot Protocol Homepage](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-compress)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl on PATH, a running Pilot Protocol daemon, and local compression tools such as gzip, zstd, lz4, or brotli.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
