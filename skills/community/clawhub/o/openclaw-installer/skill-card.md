## Description: <br>
Installs OpenClaw with commands to install the CLI, verify it, start gateway and dashboard services, and review cost and security cautions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dox012](https://clawhub.ai/user/dox012) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to install OpenClaw globally, validate the installation, start local OpenClaw services, and understand practical cost and security precautions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Global npm installation can add OpenClaw packages system-wide. <br>
Mitigation: Review the npm packages and official documentation before installing, and pin a version if reproducibility matters. <br>
Risk: OpenClaw gateway or dashboard services may be exposed if run without proper protection. <br>
Mitigation: Keep local services private or protect them with appropriate network controls before use. <br>
Risk: Paid model providers can incur unexpected API costs during agent use. <br>
Mitigation: Set API spending limits and monitor provider billing when using paid models. <br>


## Reference(s): <br>
- [OpenClaw Documentation](https://docs.openclaw.ai/) <br>
- [OpenClaw Installation Guide](https://docs.openclaw.ai/install) <br>
- [OpenClaw GitHub Repository](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
