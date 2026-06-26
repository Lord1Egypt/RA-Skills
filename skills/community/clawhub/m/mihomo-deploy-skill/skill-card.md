## Description: <br>
Deploys the mihomo proxy kernel and Metacubexd web UI on a Linux server using systemd user services without requiring sudo for the main setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rayneyael](https://clawhub.ai/user/rayneyael) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system operators use this skill to set up a persistent mihomo proxy service and local web UI on a Linux server from an existing provider config.yaml. It guides architecture detection, downloads, config patching, service setup, SSH tunneling, and proxy environment configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill deploys a persistent proxy service on a Linux server. <br>
Mitigation: Install it only when a persistent proxy service is intended, prefer the default 127.0.0.1 controller with SSH tunneling, and use a strong secret for the web UI. <br>
Risk: The setup downloads binaries and web UI assets from upstream release locations. <br>
Mitigation: Consider pinning versions or verifying upstream downloads before running them in a production or sensitive environment. <br>
Risk: The helper script modifies config.yaml in place. <br>
Mitigation: Back up config.yaml before patching and protect the provider configuration file because it may contain sensitive proxy subscription details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rayneyael/mihomo-deploy-skill) <br>
- [mihomo releases](https://github.com/MetaCubeX/mihomo/releases) <br>
- [mihomo latest release API](https://api.github.com/repos/MetaCubeX/mihomo/releases/latest) <br>
- [MetaCubeX geo database release](https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/geoip.metadb) <br>
- [Metacubexd web UI repository](https://github.com/MetaCubeX/Metacubexd.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash commands, configuration snippets, and a Python helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment guidance and in-place config patching commands; users should review generated settings before running them on a server.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
