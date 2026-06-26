## Description: <br>
Validates and runs the complete five-step Kujiale OpenAPI 3D model upload flow: STS credentials, OSS upload, model parsing, parse-status polling, and model submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[violalulu](https://clawhub.ai/user/violalulu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to test or automate Kujiale 3D model ZIP uploads with their own OpenAPI credentials. It helps validate connectivity, upload to OSS, trigger parsing, poll for completion, and submit the resulting model asset. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A real run can upload and submit a model to the user's Kujiale tenant. <br>
Mitigation: Run --dry-run first, then execute the real flow only in a trusted shell with intentional credentials and target ZIP input. <br>
Risk: The sample submit defaults for location and brand category may not match every tenant or catalog tree. <br>
Mitigation: Review and adjust the default location and brand category values before using the real submit step. <br>
Risk: Terminal or CI logs may expose operational details because the app key is printed. <br>
Mitigation: Avoid sharing logs from real runs and rotate Kujiale credentials if exposure is suspected. <br>
Risk: The real upload path requires outbound access to Kujiale OpenAPI and the returned OSS endpoint. <br>
Mitigation: Run the real flow only where network policy permits those endpoints, or keep validation to dry-run mode. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/violalulu/kujiale-3d-model-upload) <br>
- [Manycore OpenAPI console](https://www.manycoreapis.com/openapi/console/keys) <br>
- [Manycore OpenAPI homepage](https://www.manycoreapis.com/openapi/index) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Code, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-like upload summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Real runs may upload and submit a model to the user's Kujiale tenant; dry-run mode returns mock summary data without network calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
