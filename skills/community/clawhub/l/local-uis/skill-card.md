## Description:

Discover locally running HTTP interfaces, identify their listening ports and processes, and build a browsable launcher dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to discover locally running web apps, dashboards, notebooks, and development servers and open them from a generated launcher page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can be redirected outside localhost or affected by proxy settings despite starting probes at 127.0.0.1.

Mitigation: Review before installing in sensitive environments and run only where local service probing is authorized.

Risk: The generated dashboard can contain sensitive local service titles, process names, PIDs, ports, and response status.

Mitigation: Avoid sharing the dashboard and review it before publishing or moving it outside the local environment.

Risk: Running the default command may open a browser automatically.

Mitigation: Use --no-open when browser launch is not desired.

## Reference(s):

- [Local UIs ClawHub Skill Page](https://clawhub.ai/antreasantoniou/skills/local-uis)
- [README](README.md)
- [Security](SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON scanner output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scanner can write a local HTML dashboard at ~/.local/state/local-uis/dashboard.html and optionally open it in a browser.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
