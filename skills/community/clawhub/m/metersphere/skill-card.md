## Description: <br>
Integrates the MeterSphere REST API with local scripts so an OpenClaw agent can query organizations, projects, modules, test assets, reviews, and defects, and generate or write functional cases, API definitions, and API test cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fit2-zhao](https://clawhub.ai/user/fit2-zhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and test managers use this skill to automate MeterSphere test asset workflows, including querying projects and reviews, generating functional and API test cases, importing OpenAPI definitions, and producing case summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated MeterSphere credentials can allow broad read/write access to test assets. <br>
Mitigation: Use least-privilege credentials, prefer read-only keys for query workflows, and use separate limited credentials for create or batch-write workflows. <br>
Risk: Misconfigured endpoints or IDs can send data to the wrong MeterSphere instance, project, template, or version. <br>
Mitigation: Set a trusted METERSPHERE_BASE_URL and explicit METERSPHERE_PROJECT_ID, METERSPHERE_DEFAULT_TEMPLATE_ID, and METERSPHERE_DEFAULT_VERSION_ID values before write operations. <br>
Risk: Custom HTTP headers or verifier output may expose sensitive data. <br>
Mitigation: Avoid METERSPHERE_HEADERS_JSON unless required, never include unrelated authentication headers, and do not share verification output containing environment or connectivity details. <br>
Risk: Raw and write commands can modify live MeterSphere data. <br>
Mitigation: Review commands before execution and test the skill in a non-production MeterSphere environment before using production credentials. <br>


## Reference(s): <br>
- [MeterSphere ClawHub release](https://clawhub.ai/fit2-zhao/metersphere) <br>
- [fit2-zhao publisher profile](https://clawhub.ai/user/fit2-zhao) <br>
- [INSTALLATION_CHECKLIST.md](INSTALLATION_CHECKLIST.md) <br>
- [SIGNATURE_ALGORITHM.md](SIGNATURE_ALGORITHM.md) <br>
- [ms-api.md](references/ms-api.md) <br>
- [ai-functional-case-prompt.md](references/ai-functional-case-prompt.md) <br>
- [ai-api-bundle-prompt.md](references/ai-api-bundle-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, and shell command guidance for MeterSphere API workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize MeterSphere query results, generate local draft files, or execute authenticated read/write API workflows when configured with credentials.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and skill-metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
