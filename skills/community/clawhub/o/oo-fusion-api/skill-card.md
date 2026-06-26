## Description: <br>
OOMOL Fusion API lets an agent use OOMOL's Fusion API connector through the oo CLI for reading, creating, updating, deleting, and processing data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run OOMOL Fusion API actions for multimodal generation, transcription, OCR, image and video workflows, document conversion, web reading, file upload, and task status retrieval through an authenticated OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some generation and processing actions may change account state or consume paid OOMOL resources even when the action is not tagged as write. <br>
Mitigation: Ask the agent to show the exact action name and payload before generation, upload, conversion, voice, image, video, or document-processing actions. <br>
Risk: Destructive actions can remove or overwrite resources. <br>
Mitigation: Require explicit approval for the target resource before running actions tagged destructive. <br>
Risk: Incorrect payloads can trigger unintended API behavior or failed jobs. <br>
Mitigation: Inspect the live action schema with oo connector schema before constructing payloads. <br>


## Reference(s): <br>
- [OOMOL Fusion API homepage](https://www.oomol.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-fusion-api) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or retrieve URLs, generated media, converted documents, OCR text, transcripts, task states, and task results depending on the selected Fusion API action.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
