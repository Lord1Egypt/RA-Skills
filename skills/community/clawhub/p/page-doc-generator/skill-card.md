## Description: <br>
Generate Word documentation from mini-program/uni-app project screenshots and source code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skyfragments](https://clawhub.ai/user/skyfragments) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate page-level documentation for mini-program or uni-app projects by pairing Vue page files with screenshots and producing Markdown and DOCX outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated documentation may include private source code, secrets, absolute paths, or sensitive screenshots from the selected project. <br>
Mitigation: Review the Markdown and DOCX outputs before sharing and run the skill only on projects whose pages and screenshots are appropriate to disclose. <br>
Risk: Generated files may overwrite same-named documentation outputs in the target directory. <br>
Mitigation: Choose an output directory where replacing generated Markdown or DOCX files is acceptable, or preserve existing outputs before running the scripts. <br>
Risk: DOCX conversion depends on a local pandoc installation and may fail when pandoc is unavailable. <br>
Mitigation: Install pandoc and confirm it is on PATH before using the DOCX conversion step. <br>


## Reference(s): <br>
- [Pandoc](https://pandoc.org/) <br>
- [ClawHub Skill Page](https://clawhub.ai/skyfragments/page-doc-generator) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, files, shell commands, guidance] <br>
**Output Format:** [Markdown documentation and DOCX files generated from local project files and screenshots] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated Markdown and DOCX documentation in the selected project or output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
