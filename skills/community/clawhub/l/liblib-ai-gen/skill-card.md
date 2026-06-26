## Description: <br>
Generate images with Seedream4.5 and videos with Kling via the LiblibAI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xtaq](https://clawhub.ai/user/xtaq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creative operators use this skill to generate LiblibAI images and videos from text prompts or image URLs, poll asynchronous tasks, and retrieve generated media URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, private image URLs, and generated media requests are sent to LiblibAI. <br>
Mitigation: Do not submit confidential prompts, private image URLs, or sensitive media unless sharing them with LiblibAI is acceptable and its data handling terms have been reviewed. <br>
Risk: The CLI requires LiblibAI API credentials for authenticated external API calls. <br>
Mitigation: Store LIB_ACCESS_KEY and LIB_SECRET_KEY as environment secrets and review generated commands before execution. <br>
Risk: Generated image URLs are documented as expiring after 7 days. <br>
Mitigation: Download or persist required outputs promptly when retention is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xtaq/liblib-ai-gen) <br>
- [LiblibAI OpenAPI endpoint](https://openapi.liblibai.cloud) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LIB_ACCESS_KEY and LIB_SECRET_KEY; uses asynchronous task polling and returns image or video URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
