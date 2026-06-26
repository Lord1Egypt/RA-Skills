## Description: <br>
HubStudio OpenAPI skill for full endpoint lookup, request/response field explanation, and parameter constraint checking. Use when querying HubStudio API interfaces, validating request payloads, or building automation against openapi.yaml. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hubstudio-Max](https://clawhub.ai/user/hubstudio-Max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to look up HubStudio OpenAPI endpoints, validate request and response fields, and assemble local API or CLI calls for browser, cloud phone, account, and group automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over HubStudio browsers, cloud phones, cookies, accounts, files, and local API operations. <br>
Mitigation: Use a test HubStudio account first, scope actions to intended resources, and review generated request bodies before execution. <br>
Risk: Shell execution, ADB, cookie import/export, file upload, account changes, cache clearing, delete, and stop-all operations can change or expose user resources. <br>
Mitigation: Require explicit human approval before running commands for these operations and avoid using production data unless the action has been reviewed. <br>
Risk: Batch and testAll workflows can touch many endpoints or resources at once. <br>
Mitigation: Avoid running broad tests against production environments and prefer narrow endpoint checks with known safe inputs. <br>


## Reference(s): <br>
- [HubStudio API Docs](https://api-docs.hubstudio.cn/) <br>
- [ClawHub Skill Page](https://clawhub.ai/hubstudio-Max/hubstudio) <br>
- [Full Generated API Reference](reference.md) <br>
- [ADB Connection Guide](ADB_CONNECTION_GUIDE.md) <br>
- [OpenClaw Agent Browser Tutorial](OPENCLAW_AGENT_BROWSER_TUTORIAL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads, curl examples, and Node.js command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include HubStudio API request bodies and local CLI commands; require human review before executing state-changing operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
