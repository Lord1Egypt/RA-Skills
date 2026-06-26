## Description: <br>
Use the local OpenCLI source install as the primary OpenCLI skill for capability discovery, browser-bridge health checks, Twitter/X routing, and stable command invocation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoyang78](https://clawhub.ai/user/chaoyang78) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route suitable tasks through a local OpenCLI installation, including command discovery, browser bridge diagnostics, Twitter/X retrieval, public-site adapters, and external CLI passthrough. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route agent work through a local OpenCLI installation with broad command execution authority. <br>
Mitigation: Review commands before execution and install only when the intended workflow requires local OpenCLI access. <br>
Risk: Browser-backed adapters may operate through logged-in browser sessions and can expose account or session state. <br>
Mitigation: Avoid sensitive browser profiles or accounts unless necessary, and verify browser bridge health before using browser-backed adapters. <br>
Risk: External CLI passthrough commands can read or change local, repository, cloud, or account state. <br>
Mitigation: Treat passthrough commands as privileged operations and scope them to expected repositories, services, and accounts. <br>


## Reference(s): <br>
- [OpenCLI command cookbook](references/commands.md) <br>
- [Opencli release page](https://clawhub.ai/chaoyang78/opencli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers JSON output for CLI commands when available and asks agents to report exact commands when useful for reuse.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
