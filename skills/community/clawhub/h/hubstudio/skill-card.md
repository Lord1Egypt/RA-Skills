## Description:

HubStudio OpenAPI skill for full endpoint lookup, request/response field explanation, and parameter constraint checking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hubstudio-max](https://clawhub.ai/user/hubstudio-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to look up HubStudio local API endpoints, validate request and response fields, and generate CLI or curl calls for browser environment, cloud phone, account, and group automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger privileged HubStudio browser, cloud phone, account, cookie, and destructive testing actions.

Mitigation: Install only for intended HubStudio administration workflows and require human review before executing generated commands.

Risk: The testAll command can exercise many endpoints against the configured HubStudio service.

Mitigation: Do not run testAll on a real account or production workspace; use isolated test data when endpoint coverage is required.

Risk: Misconfigured HUBSTUDIO_BASE_URL could direct commands to an unintended service.

Mitigation: Keep HUBSTUDIO_BASE_URL pinned to the trusted local HubStudio service before allowing agent-driven calls.

Risk: Automation outputs may expose or manipulate secrets, cookies, or account data.

Mitigation: Avoid exporting secrets or cookies through the skill and review generated payloads before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hubstudio-max/skills/hubstudio)
- [HubStudio API Docs](https://api-docs.hubstudio.cn/)
- [OpenClaw Getting Started](https://docs.openclaw.ai/start/getting-started)
- [Generated API Reference](reference.md)
- [ADB Connection Guide](ADB_CONNECTION_GUIDE.md)
- [OpenAPI Definition](openapi.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON, JavaScript, curl, Node.js, ADB, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce HubStudio API payloads, generated CLI command suggestions, request validation notes, troubleshooting steps, and local automation examples.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, package.json, openapi.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
