## Description: <br>
Builds and deploys Nova Platform apps by helping developers scaffold enclave app code, push it to Git, trigger Nova builds, deploy live apps, verify runtime status, and optionally perform on-chain registration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zfdang](https://clawhub.ai/user/zfdang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, configure, build, and deploy Nova Platform TEE applications on sparsity.cloud. It is especially suited for app workflows that need scaffolded FastAPI enclave code, Nova API deployment guidance, attestation checks, and optional on-chain trust registration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses Nova and GitHub credentials for app deployment and repository pushes. <br>
Mitigation: Use fine-grained GitHub tokens limited to the target repository, avoid embedding tokens in remote URLs when possible, and rotate any token exposed in shell history or Git configuration. <br>
Risk: Generated or modified app code may be deployed to a live Nova environment. <br>
Mitigation: Review generated code and deployment configuration before triggering builds or production deployments. <br>
Risk: Default app configuration can allow broad outbound network access for generated Nova apps. <br>
Mitigation: Narrow egress settings for production apps to only the external services the app requires. <br>


## Reference(s): <br>
- [Nova Platform API Reference](references/nova-api.md) <br>
- [Odyn Internal API Reference](references/odyn-api.md) <br>
- [Nova Platform](https://sparsity.cloud) <br>
- [Nova API Docs](https://sparsity.cloud/api/docs) <br>
- [Nova Create-App Guide](https://sparsity.cloud/resources/nova-api/create-app-guide) <br>
- [Nova App Template](https://github.com/sparsity-xyz/nova-app-template) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline code blocks, generated project files, shell commands, and API configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate a scaffolded Nova app directory and deployment commands that require user-provided Nova and GitHub credentials.] <br>

## Skill Version(s): <br>
2.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
