## Description: <br>
Convert PDF documents to LaTeX source code using MinerU AI extraction for researchers, academics, and scientists who need to re-edit, re-typeset, or recover LaTeX markup from published papers, theses, and technical reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[decrystal](https://clawhub.ai/user/decrystal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, academics, and scientists use this skill to convert local or URL-based PDF papers into editable LaTeX, especially for math-heavy, multi-column, tabular, or scientific documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF contents submitted through the MinerU API may leave the user's machine. <br>
Mitigation: Do not process unpublished, proprietary, regulated, or confidential documents unless sharing them with MinerU/OpenDataLab has been approved. <br>
Risk: The skill requires installing and running the mineru-open-api CLI from npm or a Go repository. <br>
Mitigation: Verify the package or repository source before installation and install only in environments approved for this workflow. <br>
Risk: The workflow requires a MINERU_TOKEN credential. <br>
Mitigation: Provide the token through the environment or CLI authentication flow and avoid committing or exposing it in prompts, logs, or source files. <br>


## Reference(s): <br>
- [MinerU homepage](https://mineru.net) <br>
- [MinerU token management](https://mineru.net/apiManage/token) <br>
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU) <br>
- [ClawHub skill page](https://clawhub.ai/decrystal/pdf-to-latex-mineru) <br>
- [Publisher profile](https://clawhub.ai/user/decrystal) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of mineru-open-api to produce LaTeX output from PDF inputs, optionally saved to an output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
