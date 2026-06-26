## Description: <br>
A fully local password management skill for OpenClaw with AES-256-GCM encryption, password generation, and sensitive info detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jixsonwang](https://clawhub.ai/user/jixsonwang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to store, search, update, generate, and detect local credentials through agent tools and a command-line interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles highly sensitive secrets and may expose generated or retrieved credentials in the agent conversation. <br>
Mitigation: Treat revealed or generated secrets as sensitive chat content, avoid requesting plaintext display unless necessary, and rotate credentials if they are exposed in logs or transcripts. <br>
Risk: Using the master password through environment variables or command-line arguments can expose it to local process, shell, or automation history. <br>
Mitigation: Prefer interactive password entry for real vaults, avoid storing real master passwords in environment variables, and clear shell or CI logs after testing. <br>
Risk: The documented 48-hour cache and plaintext reveal options can leave vault access available longer than intended on shared machines. <br>
Mitigation: Review cache timeout and reveal defaults before use, lock the vault after operations, and use this release only where local filesystem permissions and device access are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jixsonwang/password-manager) <br>
- [Skill documentation](SKILL.md) <br>
- [OpenClaw hook documentation](hooks/openclaw/HOOK.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and OpenClaw tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local password-manager actions and may reveal, generate, or save sensitive credential values when requested.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
