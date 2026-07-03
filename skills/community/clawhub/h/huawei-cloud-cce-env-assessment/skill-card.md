## Description: <br>
A skill for Huawei Cloud CCE assessment that collects metrics and configurations from containerized application environments and generates assessment reports and improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to assess Huawei Cloud CCE container environments against cloud-native best practices, produce metric scoring, and identify prioritized improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to Huawei Cloud account credentials and cluster metadata. <br>
Mitigation: Use tightly scoped temporary credentials, run in an isolated environment, and remove saved credentials and generated artifacts after assessment. <br>
Risk: The workflow may request privileged local actions during dependency or tool setup. <br>
Mitigation: Review each command before approving it and avoid sudo unless the specific command is expected and necessary. <br>
Risk: The workflow accepts a repository URL for Dockerfile assessment. <br>
Mitigation: Review the repository URL before allowing clone or analysis. <br>


## Reference(s): <br>
- [Huawei Cloud KooCLI Installation Guide](references/koocli-installation-guide.md) <br>
- [Python Requirements](references/requirements.txt) <br>
- [Huawei Cloud KooCLI Documentation](https://support.huaweicloud.com/wtsnew-hcli/index.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/huaweiclouddev/huawei-cloud-cce-env-assessment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, plus generated Excel and HTML assessment files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces intermediate collection data under data/ and final assessment artifacts under artifacts/.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
