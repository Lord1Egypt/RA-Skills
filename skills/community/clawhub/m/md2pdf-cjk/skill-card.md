## Description: <br>
Converts Markdown to PDF with CJK support using WeasyPrint and Noto CJK fonts, including emoji replacement, custom CSS styling, code blocks, and tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shimonxin](https://clawhub.ai/user/shimonxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert Markdown documents into well-formatted PDFs when Chinese, Japanese, or Korean text, code blocks, tables, and emoji-safe output are required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive or untrusted Markdown may contain raw HTML or external references that affect local PDF conversion behavior. <br>
Mitigation: Review source Markdown before conversion, avoid processing unknown documents without inspection, and remove external references when sensitive content is involved. <br>
Risk: Rendering failures can produce missing, blank, or incomplete PDF output. <br>
Mitigation: Use the documented WeasyPrint and Noto CJK font workflow, write output under /tmp, and confirm the PDF exists and is larger than 10KB before sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shimonxin/md2pdf-cjk) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Files] <br>
**Output Format:** [Markdown instructions with Python, HTML/CSS, and bash snippets for producing PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs agents to write PDF output under /tmp and verify that the generated PDF exists and is larger than 10KB before sending.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
