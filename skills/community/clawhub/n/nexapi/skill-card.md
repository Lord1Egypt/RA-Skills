## Description: <br>
NexAPI 工具类接口调用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avrinbai](https://clawhub.ai/user/avrinbai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Nexapi to call NexAPI utility, data, content, and operations endpoints through a Python CLI while minimizing repeated catalog fetches and response volume. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a NexAPI key and can store it in a local configuration file. <br>
Mitigation: Keep the API key scoped and rotated, and store the configuration file in a private location with owner-only permissions. <br>
Risk: Endpoint override settings can direct requests to a non-default host or health path. <br>
Mitigation: Avoid setting the base URL or health path to untrusted hosts. <br>
Risk: The integration depends on trust in the external NexAPI service. <br>
Mitigation: Install only if you trust the API service and need this integration. <br>


## Reference(s): <br>
- [NexAPI service endpoint](https://api.avrinbai.cn) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration instructions, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to compact responses; full API responses require verbose mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
