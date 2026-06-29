## Description: <br>
Use Keeper Commander CLI and Keeper Secrets Manager workflows when installing Keeper tooling, setting up profiles, signing in, running Keeper interactively, searching vault or admin data, retrieving a specific secret or field, injecting secrets into commands, creating or updating Keeper records, or troubleshooting Keeper terminal sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keeper-security](https://clawhub.ai/user/keeper-security) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and administrators use this skill to work with Keeper Commander and Keeper Secrets Manager for setup, interactive sessions, secret injection, targeted field retrieval, record updates, and troubleshooting while minimizing secret exposure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Keeper workflows can touch vault metadata, secrets, sessions, and record updates. <br>
Mitigation: Supervise secret reads and record changes, retrieve only the exact requested field, prefer Keeper notation or injection over displaying secrets, and close tmux sessions when work is complete. <br>
Risk: Delete, clear, or remove operations can change Keeper records or administrative state. <br>
Mitigation: Require explicit user confirmation before destructive commands and verify command syntax with installed CLI help or Keeper documentation. <br>


## Reference(s): <br>
- [Keeper Commander on ClawHub](https://clawhub.ai/keeper-security/keeper-commander) <br>
- [Keeper Agent Kit](https://github.com/Keeper-Security/keeper-agent-kit) <br>
- [Keeper Docs](https://docs.keeper.io) <br>
- [Keeper Secrets Manager Overview](https://docs.keeper.io/en/keeperpam/secrets-manager/overview) <br>
- [Commander CLI Command Reference](https://docs.keeper.io/en/keeperpam/commander-cli/command-reference) <br>
- [Keeper Notation](https://docs.keeper.io/en/keeperpam/secrets-manager/about/keeper-notation) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tmux session commands and Keeper CLI checks; avoids displaying secrets unless explicitly required and appropriate.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
