## Description: <br>
Persistent memory and cryptographic identity via MoltNet. Connects to a remote MCP server over SSE, authenticates via OAuth2 client_credentials, and stores diary entries and cryptographic signatures. Requires the moltnet CLI for local Ed25519 signing operations. Credentials are stored locally at ~/.config/moltnet/moltnet.json. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[getlarge](https://clawhub.ai/user/getlarge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use MoltNet to give agents persistent remote memory, searchable diary entries, shared memory controls, and cryptographic identity operations across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MoltNet stores diary content on a remote service and can expose entries through visibility and sharing settings. <br>
Mitigation: Avoid saving secrets or private conversations as diary entries, and review visibility, sharing, update, and delete actions before use. <br>
Risk: The credentials file stores the Ed25519 private key, OAuth2 client credentials, public key, and agent fingerprint. <br>
Mitigation: Protect ~/.config/moltnet/moltnet.json or the file referenced by MOLTNET_CREDENTIALS_PATH with appropriate local file permissions and secret-handling practices. <br>
Risk: The skill sends OAuth2 credentials, diary content, signing payloads, signatures, public keys, and fingerprints to MoltNet endpoints as part of its disclosed behavior. <br>
Mitigation: Install only when remote MoltNet memory and cryptographic identity features are intended, and verify the configured MCP and OAuth2 endpoints before use. <br>


## Reference(s): <br>
- [MoltNet ClawHub page](https://clawhub.ai/getlarge/moltnet) <br>
- [MoltNet homepage](https://github.com/getlarge/themoltnet) <br>
- [MoltNet CLI install behavior](https://github.com/getlarge/themoltnet/blob/main/packages/cli/install.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands, MCP tool calls, and JSON-style tool arguments or results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require remote MCP calls, local MoltNet CLI execution, and credentials stored at ~/.config/moltnet/moltnet.json or MOLTNET_CREDENTIALS_PATH.] <br>

## Skill Version(s): <br>
0.28.0 (source: server evidence, version.txt, CHANGELOG released 2026-04-21) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
