## Description: <br>
GPT Image 2 on RunComfy generates and edits images through the RunComfy CLI using text prompts and up to 10 reference image URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to generate or edit images with GPT Image 2 via RunComfy, especially for prompts that need embedded text, signage, product imagery, ads, localization, or composition-preserving edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts and provided reference image URLs are sent to RunComfy for processing. <br>
Mitigation: Use this skill only for content acceptable under RunComfy's terms, and avoid sensitive, private, or proprietary images unless that transfer is approved. <br>
Risk: The skill requires a RunComfy token or local RunComfy login configuration. <br>
Mitigation: Keep RUNCOMFY_TOKEN and ~/.config/runcomfy private, use secret management in CI, and rotate the token if it is exposed. <br>
Risk: Ambiguous requests for "GPT Image" may select a provider the user did not intend. <br>
Mitigation: Confirm RunComfy as the intended provider when the request is ambiguous. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/gpt-image-2-runcomfy) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-image-2-runcomfy) <br>
- [GPT Image 2 text-to-image endpoint](https://www.runcomfy.com/models/openai/gpt-image-2/text-to-image?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-image-2-runcomfy) <br>
- [GPT Image 2 edit endpoint](https://www.runcomfy.com/models/openai/gpt-image-2/edit?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-image-2-runcomfy) <br>
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-image-2-runcomfy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON input examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides RunComfy CLI requests that return generated or edited image files into a caller-selected output directory.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
