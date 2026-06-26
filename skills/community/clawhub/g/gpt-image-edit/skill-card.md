## Description: <br>
Uses the local RunComfy CLI to call RunComfy's OpenAI GPT Image 2 edit endpoint for preservation-focused image edits, multilingual in-image text edits, layout changes, and multi-reference compositions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and content teams use this skill to prepare RunComfy GPT Image 2 edit requests for targeted image edits, localized in-image text changes, and multi-reference compositions while preserving important source-image details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image URLs and edit prompts are sent to RunComfy's service. <br>
Mitigation: Install and use the skill only when RunComfy is trusted for the images and prompts being processed. <br>
Risk: Private or sensitive images may be exposed through third-party image URLs or model processing. <br>
Mitigation: Avoid private or sensitive images unless RunComfy's service terms fit the intended use. <br>
Risk: The RUNCOMFY_TOKEN credential can authorize service access if disclosed. <br>
Mitigation: Protect RUNCOMFY_TOKEN and local RunComfy configuration files. <br>
Risk: Generated outputs are downloaded to a user-selected directory. <br>
Mitigation: Choose output directories deliberately and review generated files before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/gpt-image-edit) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-image-edit) <br>
- [RunComfy GPT Image 2 edit endpoint](https://www.runcomfy.com/models/openai/gpt-image-2/edit?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-image-edit) <br>
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=gpt-image-edit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON input snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the runcomfy CLI plus RUNCOMFY_TOKEN or local RunComfy configuration; generated image files are written to the selected output directory.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
