## Description: <br>
Translates Chinese PowerPoint presentations into English while preserving non-text slide content and applying business-oriented font and layout adjustments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[birkhoff-china](https://clawhub.ai/user/birkhoff-china) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, business teams, and presentation authors use this skill to translate Chinese PPTX files into English while preserving slide structure, media, charts, tables, notes, and formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presentation text from slides, tables, grouped shapes, and notes can be sent to the selected LLM endpoint. <br>
Mitigation: For confidential presentations, use a local or organization-approved endpoint and avoid untrusted custom API bases. <br>
Risk: Cloud or third-party endpoints may require an API key and may retain or process submitted slide text under their own terms. <br>
Mitigation: Use a revocable, least-privilege API key and confirm the endpoint's data-handling policy before translating sensitive decks. <br>
Risk: The skill installs and runs Python dependencies to read and write PowerPoint files. <br>
Mitigation: Install dependencies in a virtual environment and review the translated output before sharing or publishing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/birkhoff-china/ppt-translate) <br>
- [PPT Translation Tool - Technical Reference](reference.md) <br>
- [Skill definition](SKILL.md) <br>
- [Ollama](https://ollama.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with command-line examples; the bundled script writes a translated PPTX file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, python-pptx, requests, an input .pptx file, and a local or cloud OpenAI-compatible LLM endpoint.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
