## Description: <br>
Provides a Python CLI and SDK for image analysis, OCR text extraction, copywriting, and multimodal chat with a Moonshot-compatible API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mendynew](https://clawhub.ai/user/mendynew) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to route image analysis, OCR extraction, marketing copy generation, and multimodal chat tasks through a local Python CLI or SDK after configuring an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images, documents, OCR content, prompts, and chat messages may be sent to the configured external API provider. <br>
Mitigation: Use a dedicated API key, review selected inputs before invocation, and avoid sensitive or regulated files unless approved. <br>
Risk: Broad image, OCR, copywriting, and chat triggers could cause the skill to run when the user did not intend to send content externally. <br>
Mitigation: Confirm the skill is intentionally invoked before using image, OCR, or multimodal chat features. <br>
Risk: The package installs and runs third-party Python code and dependencies. <br>
Mitigation: Install dependencies in an isolated environment and review commands and files before execution. <br>


## Reference(s): <br>
- [Moonshot Platform](https://platform.moonshot.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/mendynew/moonshot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown, plain text, JSON, and Python or shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save OCR or copywriting results to user-specified files; image and OCR features can send selected inputs to an external API.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, skill frontmatter, target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
