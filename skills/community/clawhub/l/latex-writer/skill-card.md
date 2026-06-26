## Description: <br>
Generate professional LaTeX documents from templates. Supports academic papers (IEEE/ACM), Chinese thesis (CTeX), CVs (moderncv), and custom templates. Auto-compile to PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alicepub](https://clawhub.ai/user/alicepub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, students, and document authors use this skill to turn structured content into LaTeX source and compiled PDFs for academic papers, Chinese theses and reports, CVs, resumes, and custom template-based documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or user-provided LaTeX content and custom class or style templates are compiled locally. <br>
Mitigation: Review generated .tex content before compiling important or sensitive documents, use only trusted .cls and .sty templates, and sandbox LaTeX received from untrusted sources. <br>
Risk: PDF generation depends on a local TeX installation and its installed packages, fonts, and security updates. <br>
Mitigation: Keep the TeX distribution current and confirm required packages and fonts are installed before relying on compiled output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alicepub/latex-writer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance, LaTeX source code, and generated .tex/.pdf files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local TeX distribution such as TeX Live or MiKTeX with xelatex for PDF compilation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
