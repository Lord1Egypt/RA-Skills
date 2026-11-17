## Description:

Deploy mihomo proxy kernel + Metacubexd web UI on a Linux server without sudo by using systemd --user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rayneyael](https://clawhub.ai/user/rayneyael)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy a user-scoped Mihomo proxy service and Metacubexd web UI on Linux, including config patching, systemd user service setup, SSH tunneling, and proxy environment setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote binaries and web UI assets may change after release.

Mitigation: Pin Mihomo and Metacubexd to reviewed versions and verify checksums before execution.

Risk: The external controller can be exposed if bound to 0.0.0.0.

Mitigation: Keep the controller bound to 127.0.0.1 by default, use SSH tunneling, and require firewall controls plus a strong secret for any wider exposure.

Risk: A persistent proxy daemon and shell startup changes can alter network routing.

Mitigation: Review systemd user services, shell startup edits, proxy variables, and no_proxy values before enabling persistence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rayneyael/skills/mihomo-deploy-skill)
- [MetaCubeX Mihomo releases](https://github.com/MetaCubeX/mihomo/releases)
- [MetaCubeX Metacubexd](https://github.com/MetaCubeX/Metacubexd)
- [MetaCubeX meta-rules-dat geo database](https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/geoip.metadb)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown with inline bash and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes in-place configuration patching guidance and persistent systemd user service setup.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
