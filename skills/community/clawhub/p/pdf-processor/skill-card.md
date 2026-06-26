## Description: <br>
Processes academic PDFs by extracting text, detecting language, translating English papers to Chinese with a local Ollama model, and generating concise Chinese summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reaperchen](https://clawhub.ai/user/reaperchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and document-processing users use this skill to run a local workflow that extracts academic PDF text, translates English papers into Chinese, produces short Chinese summaries, and organizes the resulting files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow moves original PDFs and deletes temporary extraction files during processing. <br>
Mitigation: Run it in a dedicated working folder and back up important originals before processing. <br>
Risk: The script may start a local Ollama service in the background. <br>
Mitigation: Start and manage Ollama yourself when operating in sensitive or controlled environments. <br>
Risk: Progress data is stored in plaintext while processing. <br>
Mitigation: Avoid processing sensitive documents unless the local folder permissions and retention behavior are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/reaperchen/pdf-processor) <br>
- [PDF processing workflow](references/workflow.md) <br>
- [PDF processing directory structure](references/directory-structure.md) <br>
- [Ollama](https://ollama.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus generated text, JSON index files, and local text output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include translated text files, summary text files, plaintext progress JSON during processing, and optional paper index JSON.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
