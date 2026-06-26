## Description: <br>
Set up and use Bitwarden CLI (bw) for installing the CLI, unlocking a vault, and reading or generating secrets with BW_SESSION session management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JimiHFord](https://clawhub.ai/user/JimiHFord) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to set up and operate the Bitwarden CLI for focused vault lookups, password generation, and authenticated session management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may handle password-vault data when asked to run authenticated Bitwarden CLI commands. <br>
Mitigation: Prefer narrow lookups over broad vault listing, avoid sharing captured command output, and lock Bitwarden when finished. <br>
Risk: A persistent BW_SESSION can remain available after the requested vault task is complete. <br>
Mitigation: Run authenticated Bitwarden commands in a dedicated tmux session, then kill that session and lock the vault after use. <br>
Risk: Optional local testing with Docker Compose or scripts can change local services and test data. <br>
Mitigation: Review optional Docker Compose files and scripts before running them, and use local test credentials only for testing. <br>


## Reference(s): <br>
- [Bitwarden CLI documentation](https://bitwarden.com/help/cli/) <br>
- [Vaultwarden project](https://github.com/dani-garcia/vaultwarden) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bitwarden CLI (bw) and tmux; authenticated vault commands depend on BW_SESSION.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
