## Description: <br>
OpenAPI/Swagger security auditor that scans OpenAPI 3.x or Swagger 2.0 specs for common authentication, transport, credential-handling, OAuth, sensitive-data, validation, authorization, upload, scope, and auth-response misconfigurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to audit OpenAPI and Swagger specifications from files, directories, or public URLs before release or CI enforcement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad directory scans or public URL scans may process unintended OpenAPI or Swagger specifications. <br>
Mitigation: Use the skill only on intended files or trusted public spec URLs, and avoid broad directory scans unless needed. <br>
Risk: CI use can run the embedded audit script in build environments. <br>
Mitigation: Verify the embedded script and dependency setup before enabling the skill in CI. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-openapi-sec-audit) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with security findings, shell command examples, and CI configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include severity-filtered OpenAPI audit results and CI exit behavior guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
