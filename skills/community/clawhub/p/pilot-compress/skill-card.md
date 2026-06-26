## Description: <br>
Transparent compression for large messages over the Pilot Protocol network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to compress large text, JSON, binary payloads, or files before sending them over Pilot Protocol and to decompress received compressed payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compressed payloads sent over Pilot Protocol may contain sensitive data, and gzip or base64 encoding does not provide encryption. <br>
Mitigation: Verify the recipient and transport security before sending sensitive data, and do not treat compression or base64 encoding as confidentiality protection. <br>
Risk: Compression can add overhead or latency for small messages, already-compressed files, or real-time streaming use cases. <br>
Mitigation: Use this skill for large payloads where bandwidth reduction is useful, and avoid it for small, already-compressed, or latency-sensitive transfers. <br>


## Reference(s): <br>
- [Pilot Protocol Homepage](https://pilotprotocol.network) <br>
- [Pilot Compress on ClawHub](https://clawhub.ai/teoslayer/pilot-compress) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, a running Pilot Protocol daemon, and compression tools such as gzip, zstd, lz4, or brotli.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
