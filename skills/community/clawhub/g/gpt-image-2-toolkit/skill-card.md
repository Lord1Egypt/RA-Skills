## Description: <br>
Install, verify, repair, and diagnose GPT-Image-2 support for OpenClaw so agents can use model refs like hnbc/gpt-image-2 through the built-in image_generate tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevins9527](https://clawhub.ai/user/kevins9527) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and validate an OpenClaw image-generation provider that exposes hnbc/gpt-image-2 through image_generate. It also helps diagnose provider registration, gateway reload, credential, and supported geometry issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or reinstalling the skill overwrites the existing local hnbc provider folder. <br>
Mitigation: Back up any custom files under ~/.openclaw/extensions/hnbc before running the installer. <br>
Risk: HNBC API credentials and image prompts are sent to the configured HNBC service during generation. <br>
Mitigation: Keep the HNBC API key private and use only a trusted HNBC base URL. <br>
Risk: The running OpenClaw gateway may keep an old provider registry after installation. <br>
Mitigation: Verify with image_generate(action="list") and restart the gateway only with user approval if the local runtime sees hnbc but the tool list does not. <br>
Risk: Requests that include unsupported resolution overrides or edit-mode inputs can fail. <br>
Mitigation: Use supported size or aspectRatio values only and use this provider for generation rather than edit workflows. <br>


## Reference(s): <br>
- [GPT-Image-2 for OpenClaw](https://clawhub.ai/kevins9527/gpt-image-2-toolkit) <br>
- [Release 1.0.1 Plan](references/release-1.0.1.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [HNBC API Base URL](https://api.1415.xin/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration notes, and JavaScript plugin files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install or replace the local hnbc OpenClaw provider and uses HNBC API credentials during image generation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
