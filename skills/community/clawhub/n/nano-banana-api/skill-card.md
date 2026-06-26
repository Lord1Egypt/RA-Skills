## Description: <br>
Generate images through the Nano Banana REST API and help agents integrate or operate the service safely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdhjkagbjksg](https://clawhub.ai/user/sdhjkagbjksg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate images, inspect available Nano Banana models, check account credits, choose sync, stream, or async generation flows, poll jobs, and produce reproducible API calls or scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An undocumented endpoint override can send the API key to a server other than the official Nano Banana API. <br>
Mitigation: Before use, leave NANO_BANANA_BASE_URL unset or confirm it points to the official API, and prefer a limited API key when available. <br>
Risk: Generated image URLs are downloaded to local storage when a download directory is supplied. <br>
Mitigation: Download outputs only into a dedicated folder and review files before reusing or sharing them. <br>


## Reference(s): <br>
- [Nano Banana official website](https://www.nananobanana.com) <br>
- [Nano Banana API Reference](references/api-reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/sdhjkagbjksg/nano-banana-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON API payloads, and generated image file paths when downloads are requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the Nano Banana REST API with an API key and optionally download returned image URLs into a dedicated local folder.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
