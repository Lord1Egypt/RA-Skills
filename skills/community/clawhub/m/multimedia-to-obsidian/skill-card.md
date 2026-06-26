## Description: <br>
Imports multimedia documents into an Obsidian vault by extracting pages or images from PPT, PDF, DOCX, and image files, sending them to a selected multimodal model, and writing generated descriptions as Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aidescend](https://clawhub.ai/user/aidescend) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Knowledge workers, developers, and Obsidian users use this skill to turn slides, PDFs, documents, and images into organized Markdown notes with model-generated content descriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents, extracted pages, or images may be sent to MiniMax, OpenAI, or Anthropic using the user's API key. <br>
Mitigation: Use the skill only with content approved for the selected external provider, avoid confidential or regulated files unless approved, and configure only the intended model credentials. <br>
Risk: The skill writes generated Markdown into a user-selected Obsidian vault or category. <br>
Mitigation: Use a narrow source directory, use simple category names without slashes or traversal, and review generated Markdown before relying on or publishing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aidescend/multimedia-to-obsidian) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files and command-line instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated descriptions into the selected Obsidian vault/category and may call MiniMax, OpenAI, or Anthropic vision APIs using user-provided API keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
