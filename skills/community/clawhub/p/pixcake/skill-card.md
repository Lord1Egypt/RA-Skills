## Description:

Pixcake Skills helps agents operate the PixCake desktop client for project lookup and creation, image import, preset retouching, export submission, and export status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasperdon](https://clawhub.ai/user/jasperdon)

### License/Terms of Use:

MIT-0

## Use Case:

External PixCake users and agent operators use this skill to route desktop-client requests into supported workflows for project management, preset retouching, and export. It helps the agent check setup, select documented PixCake MCP tools, and avoid unsupported or ambiguous operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can install mcporter globally and modify the persistent OpenClaw mcporter configuration.

Mitigation: Run check-only mode first, avoid elevated privileges, back up the existing mcporter config, and review changes before allowing setup to write configuration.

Risk: Path auto-discovery can register an unintended PixCake or pixcake-mcp executable when local installations are ambiguous.

Mitigation: Prefer explicitly supplied, known PixCake and pixcake-mcp paths and confirm the registered server with mcporter list before invoking PixCake tools.

Risk: Export submission is asynchronous and can be mistaken for completed export output.

Mitigation: Describe export submission as task creation until get_task_status confirms completion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jasperdon/skills/pixcake)
- [README](README.md)
- [Capability Map](references/capabilities.md)
- [Compatibility](references/compatibility.md)
- [MCPorter Setup](references/mcp-setup.md)
- [Projects](references/projects.md)
- [Retouch](references/retouch.md)
- [Export](references/export.md)
- [Response Policy](references/response-policy.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with bash and PowerShell command examples, plus JSON-oriented PixCake MCP calls through mcporter]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets macOS and Windows, requires PixCake 9.0.0 or newer, and routes only documented project, preset retouching, and export workflows.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
