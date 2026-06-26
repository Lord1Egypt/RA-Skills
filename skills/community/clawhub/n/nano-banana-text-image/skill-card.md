## Description: <br>
Generates images from text prompts using AtlasCloud's Nanobanana 2 text-to-image model and returns the generated image URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guilherme-funchal](https://clawhub.ai/user/guilherme-funchal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate images from descriptive text prompts through AtlasCloud's Nanobanana model. It is suited for agent workflows that prepare generation parameters, call the Node.js helper, and report the returned image URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AtlasCloud API token and asks for it to be retained for later use. <br>
Mitigation: Use a disposable or scoped token, rotate it after testing, and avoid storing long-lived credentials in shared agent memory. <br>
Risk: Prompts are sent to AtlasCloud and generation metadata or URLs are written locally. <br>
Mitigation: Avoid sensitive prompts unless token storage and local logging are clearly controlled, and review generated files before sharing or retaining them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guilherme-funchal/nano-banana-text-image) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Text response with an image URL, plus local JSON and text result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and an AtlasCloud API token; writes generation metadata and the latest image URL locally.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
