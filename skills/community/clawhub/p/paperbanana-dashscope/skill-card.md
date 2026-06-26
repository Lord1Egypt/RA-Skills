## Description: <br>
Generate academic figures and scientific diagrams from paper text using a multi-agent pipeline powered by Alibaba Cloud DashScope. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zdywrnm](https://clawhub.ai/user/zdywrnm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and academic authors use this skill to configure and run PaperBanana-DashScope for generating diagrams, plots, architecture figures, and academic illustrations from paper text and captions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential confusion because the DashScope setup uses an OpenAI-named environment variable and config key. <br>
Mitigation: Use a dedicated low-privilege DashScope key, do not reuse an OpenAI key, and verify where the key is sent before running the CLI. <br>
Risk: Persistent plaintext API key storage may expose credentials if the config file is not protected. <br>
Mitigation: Prefer an environment variable for short-lived sessions, or restrict permissions on ~/.paperbanana-dashscope/config.yaml if a config file is required. <br>
Risk: The security review verdict is suspicious for this release. <br>
Mitigation: Install only after reviewing the referenced npm package and confirming the CLI behavior matches the intended DashScope workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zdywrnm/paperbanana-dashscope) <br>
- [npm package](https://www.npmjs.com/package/paperbanana-dashscope) <br>
- [Project source link](https://github.com/TashanGKD/PaperBanana-DashScope) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands; generated figures are written as PNG files by the referenced CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a DashScope API key; figure output path, task type, model, aspect ratio, candidate count, and critic rounds are user-configurable.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
