## Description: <br>
Generate AI mockup generator images with AI via the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wkl-nieta](https://clawhub.ai/user/wkl-nieta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate product mockup images from text prompts, optionally with size settings or a reference image UUID, and receive a direct image URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference image identifiers, and generated-image requests are sent to a third-party image generation service. <br>
Mitigation: Use the skill only with prompts and references suitable for that service, and avoid private, confidential, or sensitive image inputs. <br>
Risk: The skill requires a Neta API token, and command-line token handling can expose credentials through shell history, logs, or shared terminals. <br>
Mitigation: Use a limited token, keep it out of logs and shared shells, rotate it if exposed, and install only when you trust the publisher and the Neta/talesofai service. <br>


## Reference(s): <br>
- [Mockup Gen Skill on ClawHub](https://clawhub.ai/wkl-nieta/mockup-gen-skill) <br>
- [Publisher profile: wkl-nieta](https://clawhub.ai/user/wkl-nieta) <br>
- [Neta API access](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text URL with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a generated image URL; requires a Neta API token and sends prompts or reference image UUIDs to the Neta/talesofai service.] <br>

## Skill Version(s): <br>
1.8.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
