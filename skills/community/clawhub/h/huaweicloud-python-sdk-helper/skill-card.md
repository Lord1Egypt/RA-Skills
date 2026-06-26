## Description: <br>
Helps developers inspect installed Huawei Cloud Python SDK packages, client classes, API methods, request parameters, SDK class details, and keyword matches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jupiter-19](https://clawhub.ai/user/jupiter-19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers working with Huawei Cloud Python SDK use this skill to quickly locate service packages, client classes, API methods, request fields, response classes, and credential patterns without manually searching documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper imports installed Huawei Cloud SDK modules and can resolve class paths, so untrusted packages or arbitrary module paths could execute code during import. <br>
Mitigation: Run it in a trusted Python environment, install SDK packages from trusted sources, and avoid arbitrary fully qualified class paths unless the installed module is trusted. <br>
Risk: Lookup results can be incomplete when a service package, SDK version, client class, or Request metadata is unavailable. <br>
Mitigation: Confirm missing or unclear API details in Huawei Cloud API Explorer before using the result in production code. <br>


## Reference(s): <br>
- [Huawei Cloud Python SDK GitHub](https://github.com/huaweicloud/huaweicloud-sdk-python-v3) <br>
- [Huawei Cloud API Explorer](https://apiexplorer.developer.huaweicloud.com/apiexplorer/overview) <br>
- [Credential Reference](references/knowledge.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured JSON when the helper script is invoked with --json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
