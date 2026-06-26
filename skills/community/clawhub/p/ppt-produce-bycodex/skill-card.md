## Description: <br>
Create and iterate enterprise application software solution PPTs as full-page PNG slides and optional PPTX decks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javastarboy](https://clawhub.ai/user/javastarboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, consultants, and developers use this skill to plan, generate, review, repair, and package enterprise solution presentation slides as PNG pages and optional PPTX decks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may read local OpenAI-compatible API settings and use sensitive credentials. <br>
Mitigation: Review commands that read shell configuration, keep credentials out of prompts and files, and install only when the configured model provider is acceptable for the intended slide content. <br>
Risk: Slide prompts, screenshots, or images may be sent to an external model provider during generation or repair. <br>
Mitigation: Use only approved source materials, avoid confidential business data unless the provider is authorized, and follow the skill's guidance to stop oversized retries instead of resending large artifacts. <br>
Risk: Generated presentation content may contain incorrect text, visual artifacts, or misleading business claims. <br>
Mitigation: Review contact sheets and final PNG pages before PPTX assembly, verify dimensions and transparency with the bundled checker, and keep business claims aligned with reviewed source material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/javastarboy/ppt-produce-bycodex) <br>
- [PPT production guide](references/ppt-production-guide.md) <br>
- [Enterprise solution title-bar template](references/titlebar-template.md) <br>
- [Too-large handoff template](references/too-large-handoff-template.md) <br>
- [Author blog](https://www.yuque.com/lhyyh) <br>
- [LLM tutorial](https://www.yuque.com/lhyyh/ai/llm-wiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file paths, prompts, shell commands, generated slide assets, and optional PPTX packaging instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce full-page PNG slide files, contact sheets, outline or scheme Markdown, scratch scripts, and optional PPTX decks under the user-provided project workspace.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
