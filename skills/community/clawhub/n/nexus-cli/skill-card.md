## Description: <br>
Manage a Jellyfin/Plex + *Arr media server stack: check status, add content, monitor downloads, diagnose issues, and restart services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxtechera](https://clawhub.ai/user/maxtechera) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate a self-hosted media server stack through the Admirarr CLI, including service status, diagnostics, content search, downloads, indexer setup, and stack maintenance. It is intended for environments where the user authorizes administrative media-stack and Docker actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer a media stack and Docker environment, including restarts and configuration changes. <br>
Mitigation: Require explicit user intent for setup, restart, fix, and other management actions; review planned commands before execution. <br>
Risk: The skill can collect or use local service API keys and configuration files. <br>
Mitigation: Restrict API keys to the minimum required privileges and protect ~/.config/admirarr/config.yaml and compose .env files with appropriate file permissions. <br>
Risk: Download removal and automated fix modes can change or delete operational data. <br>
Mitigation: Avoid auto/fix modes and delete-file options unless the user has confirmed the change and understands the effect. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/maxtechera/nexus-cli) <br>
- [Admirarr README](artifact/README.md) <br>
- [Agent reference](artifact/AGENTS.md) <br>
- [Recommended indexers](artifact/docs/recommended-indexers.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and references to JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read commands support JSON output for agent parsing; management commands may change Docker services, downloads, and media-stack configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
