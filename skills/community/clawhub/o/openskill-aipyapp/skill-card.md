## Description: <br>
AIPyApp is an AI-driven Python automation skill that helps install and configure aipyapp, then run natural-language tasks for web scraping, file processing, content conversion, and generated Python execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[riverfor](https://clawhub.ai/user/riverfor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to operate AIPyApp for automating Python-based tasks from natural language, including scraping pages, processing files, converting content, and running generated scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Python or task plans can run with broad local authority and may make unintended changes. <br>
Mitigation: Review generated code before execution and run tasks in a container, virtual environment, or other low-privilege workspace. <br>
Risk: Installation guidance includes unpinned package installation and system-package override behavior. <br>
Mitigation: Prefer a virtual environment, avoid --break-system-packages where possible, and pin and verify the aipyapp package version before use. <br>
Risk: LLM API keys and task outputs may be exposed through configured providers or result sharing. <br>
Mitigation: Use a dedicated low-privilege API key, disable result sharing and auto-install unless needed, and avoid sending sensitive data in prompts. <br>


## Reference(s): <br>
- [AIPyApp configuration reference](references/config.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce generated Python, dependency installation commands, and execution results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
