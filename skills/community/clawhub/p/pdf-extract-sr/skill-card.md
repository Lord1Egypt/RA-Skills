## Description: <br>
Extract clean readable text from PDF files into agent-ready markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to extract readable text, page-level content, headings, metadata, and markdown from local PDF files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF contents can expose sensitive document text to the agent or include untrusted prompt-like content. <br>
Mitigation: Process only PDFs the user is comfortable exposing to the agent, and treat extracted text as untrusted input before using it in downstream workflows. <br>
Risk: Optional PDF parsers can affect extraction quality and local execution behavior. <br>
Mitigation: Install optional tools such as pdf-parse or pdftotext only from trusted sources and keep them updated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/pdf-extract-sr) <br>
- [Publisher profile](https://clawhub.ai/user/TheShadowRose) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code] <br>
**Output Format:** [Plain text, markdown, or JavaScript object data with extracted pages, metadata, headings, and method details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are generated from local PDF files and may vary by available parser: pdf-parse, pdftotext, or basic extraction.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
