## Description: <br>
Documentation-only master skill for GLM ecosystem discovery and installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaredforreal](https://clawhub.ai/user/jaredforreal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this guide to discover GLM OCR, image, and vision skills, choose the relevant downstream skill, and follow installation or source-reference instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Following catalog commands may install downstream GLM skills with different behavior and requirements than this guide-only skill. <br>
Mitigation: Review and scan each downstream skill before installation, and avoid bulk-installing skills that are not needed. <br>
Risk: Downstream GLM skills may require a ZHIPU_API_KEY, which could be exposed if stored insecurely. <br>
Mitigation: Keep the API key in a secure environment variable or secret store, never hardcode it, and rotate or revoke unused keys. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jaredforreal/glm-master-skill) <br>
- [GLM Master Skill homepage](https://github.com/zai-org/GLM-skills/tree/main/skills/glm-master-skill) <br>
- [BigModel API documentation](https://docs.bigmodel.cn/) <br>
- [GLM-5](https://github.com/zai-org/GLM-5) <br>
- [GLM-OCR](https://github.com/zai-org/GLM-OCR) <br>
- [GLM-Image](https://github.com/zai-org/GLM-Image) <br>
- [GLM-V](https://github.com/zai-org/GLM-V) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with tables and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; does not execute scripts or subprocess commands.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
