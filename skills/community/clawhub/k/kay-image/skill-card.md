## Description: <br>
Kay Image helps agents generate or edit images and analyze images or videos through KIE AI, with optional LaoZhang-backed understanding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[papayalove](https://clawhub.ai/user/papayalove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to generate images from prompts, transform reference images, and run image or video understanding from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected image or video inputs are sent to external AI APIs. <br>
Mitigation: Use only media and prompts that are allowed under the user's privacy and compliance requirements. <br>
Risk: Optional understanding modes can use KIE AI or LaoZhang credentials, while the manifest declares only KIE_API_KEY. <br>
Mitigation: Configure only the provider credentials intended for the workflow and verify which provider flag is used before execution. <br>


## Reference(s): <br>
- [Kay Image on ClawHub](https://clawhub.ai/papayalove/kay-image) <br>
- [KIE AI](https://kie.ai/) <br>
- [LaoZhang API endpoint](https://api.laozhang.ai/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; generated images are saved as local files and understanding results are text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KIE_API_KEY for generation; KIE_UNDERSTANDING_API_KEY or LAOZHANG_API_KEY may be needed for understanding modes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact changelog top entry is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
