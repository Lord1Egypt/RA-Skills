## Description: <br>
hivulse蜂巢 AI 是一款面向软件开发的自动化技术文档生成工具，通过指定目录代码一键生成多种规范化技术文档。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mojo-bo-coder](https://clawhub.ai/user/mojo-bo-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to upload a selected project directory to Hivulse's cloud service and generate standardized technical documents such as requirements, design, test, and security self-assessment reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload a broad project directory to Hivulse's cloud service. <br>
Mitigation: Run it only on a narrow, sanitized directory and remove secrets, customer data, proprietary files, certificates, and other sensitive material before upload. <br>
Risk: The skill requires and stores or reads a Hivulse API key. <br>
Mitigation: Verify where the API key is configured, keep it out of project source files, and rotate it if it may have been exposed. <br>
Risk: Users may not see the exact file set before upload. <br>
Mitigation: Prefer a review step that lists the files and destination service before executing the upload workflow. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/mojo-bo-coder/hivulse-generate-tech-docs) <br>
- [Hivulse website](https://www.hivulse.com) <br>
- [Hivulse cloud service](https://cloud.hivulse.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line text generated through Hivulse cloud API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Hivulse API key and a project directory; generated documents are delivered after files are uploaded to the cloud service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
