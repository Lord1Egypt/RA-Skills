## Description: <br>
Helps an agent convert audio or voice recordings to text by providing `miaoda-studio-cli speech-to-text` command guidance for multiple languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nice1234-h](https://clawhub.ai/user/nice1234-h) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to select and run speech-to-text CLI commands for transcribing authorized audio recordings into plain text or JSON. It covers common language codes, output format choices, and common mistakes such as mismatched language settings or overly long recordings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio may be processed through an external CLI workflow, creating privacy and retention concerns for sensitive recordings. <br>
Mitigation: Use only audio the user is authorized to transcribe, avoid confidential recordings unless processing and retention are understood, and review the command before execution. <br>
Risk: The skill depends on the availability and trustworthiness of `miaoda-studio-cli`. <br>
Mitigation: Install the CLI only from a trusted source, verify it before use, and check file paths, language codes, and output options when a command fails. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and parameter tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide the agent to request plain text or JSON transcript output from `miaoda-studio-cli`.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
