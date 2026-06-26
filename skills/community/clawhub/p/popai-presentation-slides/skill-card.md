## Description: <br>
Creates PowerPoint presentations through the PopAI API from a topic, reference files, URLs, or a PPTX template, with support for follow-up modifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[popaiofficial](https://clawhub.ai/user/popaiofficial) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and presentation authors use this skill to generate or revise PPT decks with PopAI from prompts, source files, URLs, or an existing template. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a PopAI access token and the source guidance suggests storing it in a plaintext agent memory file. <br>
Mitigation: Store POPAI_ACCESS_TOKEN only in a protected environment variable or secret manager; do not save it in TOOLS.md, and rotate the token if it was already stored or shared. <br>
Risk: Presentation prompts, URLs, templates, and selected reference files are sent to PopAI and S3 during generation. <br>
Mitigation: Use the skill only with data approved for PopAI/S3 processing, and avoid uploading sensitive or restricted source material unless that transfer is permitted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/popaiofficial/popai-presentation-slides) <br>
- [PopAI skill setup](https://www.popai.pro/popai-skill) <br>
- [PopAI web editor](https://www.popai.pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-line progress events; final results include a PPTX download URL, web editing URL, preview image URLs, and summary text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POPAI_ACCESS_TOKEN; may upload user-selected reference files or templates to PopAI/S3; supports up to five reference files and multi-round modifications by channel ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
