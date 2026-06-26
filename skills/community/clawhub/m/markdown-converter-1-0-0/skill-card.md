## Description: <br>
Convert documents and files to Markdown using markitdown for LLM processing or text analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyingzhuangk](https://clawhub.ai/user/zhangyingzhuangk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to convert common document, data, web, media, archive, and URL inputs into Markdown for LLM processing or text analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Azure Document Intelligence and YouTube inputs may send content to external services. <br>
Mitigation: Avoid confidential documents unless the chosen conversion path is approved for that data, and prefer local conversion for sensitive files. <br>
Risk: Third-party plugins can change conversion behavior or expand the trusted code surface. <br>
Mitigation: Enable plugins only when the installed plugins are trusted and needed for the conversion task. <br>
Risk: Complex PDFs, OCR, and transcription outputs can be incomplete or inaccurate. <br>
Mitigation: Review the generated Markdown before using it for analysis, automation, or downstream LLM processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangyingzhuangk/markdown-converter-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown instructions with bash command examples; converted content is Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The converter can write Markdown to stdout or an output file and may use optional plugins or external services when enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
