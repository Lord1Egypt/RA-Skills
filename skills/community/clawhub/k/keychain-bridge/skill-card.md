## Description: <br>
Manage secrets through macOS Keychain instead of plaintext files, with migration, audit, read/write, file-bridge, and diagnostic workflows for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Euda1mon1a](https://clawhub.ai/user/Euda1mon1a) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to move macOS-hosted OpenClaw secrets into Keychain, audit for plaintext leaks, diagnose Keychain access failures, and bridge selected secrets back to files when bash tools require them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles high-value secrets and can lead an agent to access macOS Keychain and ~/.openclaw/secrets. <br>
Mitigation: Review before installing, use only on macOS accounts where that access is acceptable, and avoid broad read or get-secret requests. <br>
Risk: Some workflows can recreate plaintext credential files on disk for bash compatibility. <br>
Mitigation: Run migrations with --dry-run first, review the hard-coded Group B service list, and avoid populate_secrets.sh unless the bash tools truly require plaintext files. <br>
Risk: Keychain migrations depend on local Python keyring setup and per-binary access behavior. <br>
Mitigation: Verify keyring availability for each Python version and keep original secret files until migration and read-back verification succeed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/Euda1mon1a/keychain-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python snippets, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local macOS Keychain and filesystem workflows; no network endpoints are described in the artifact.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
