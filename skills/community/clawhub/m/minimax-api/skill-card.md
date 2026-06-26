## Description: <br>
Provides image understanding and web search via MiniMax's Token Plan API for image analysis, information extraction, and web lookup tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthew77](https://clawhub.ai/user/matthew77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to analyze images from URLs or local files, extract visual information, and perform real-time web searches through MiniMax APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, image URLs, prompts, and search queries are sent to MiniMax for processing. <br>
Mitigation: Use the skill only with data that is approved for MiniMax processing, and avoid confidential screenshots or documents. <br>
Risk: A MiniMax API key is required and can be exposed if passed on the command line. <br>
Mitigation: Store the key in a controlled secret or environment variable instead of shell history or shared command logs. <br>
Risk: Local image files are base64-encoded and uploaded for image understanding. <br>
Mitigation: Review local files before use and avoid submitting sensitive or regulated content unless that transfer is approved. <br>


## Reference(s): <br>
- [MiniMax Token Plan API Specification](references/api_spec.md) <br>
- [MiniMax Platform](https://platform.minimaxi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Plain text and formatted search results, with JSON API responses handled by helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Image inputs may be local files, HTTP/HTTPS URLs, or data URLs; search inputs are query strings.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
