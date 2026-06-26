## Description: <br>
Automate WeChat Mini Program code upload, preview, npm build, and cloud deployments with CI/CD support using Node.js or CLI without opening DevTools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to automate WeChat Mini Program and mini game CI/CD workflows, including upload, preview QR generation, npm builds, and cloud deployment tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WeChat upload private keys are deployment credentials and could be exposed through repositories, logs, or chat history. <br>
Mitigation: Store keys in a CI secret manager, pass only paths or injected secret values at runtime, keep keys out of source control and chat logs, restrict access and IPs where possible, and rotate keys if exposed. <br>
Risk: Upload, preview, cloud function, storage, and container deployment commands can change WeChat project or cloud resources. <br>
Mitigation: Require explicit operator confirmation before execution and review app IDs, project paths, robot numbers, cloud environment IDs, and deployment settings for the intended target. <br>
Risk: Cloud deployment workflows may upload unintended local files or dependencies. <br>
Mitigation: Review project paths, cloud function paths, container build directories, and ignore patterns before deployment; prefer remote npm install when appropriate to avoid uploading local dependency folders. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlark/miniprogram-ci) <br>
- [CLI Command Reference](references/cli.md) <br>
- [Cloud Development API Reference](references/cloud.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands and configuration values that require project paths, app IDs, private key paths, robot numbers, cloud environment IDs, and deployment settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
