## Description: <br>
Provides LaTeX guidance for centering verbatim code blocks and ASCII art by wrapping the verbatim environment with varwidth and center. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bg1avd](https://clawhub.ai/user/bg1avd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Document editors and developers use this skill when LaTeX verbatim blocks, code samples, or ASCII diagrams need to be horizontally centered in TeX Live documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The provided snippet globally changes LaTeX verbatim behavior and may affect documents that rely on default verbatim formatting or compatible packages. <br>
Mitigation: Review the snippet before applying it, test the document output, and avoid combining it with conflicting verbatim packages unless you adapt the configuration. <br>
Risk: The guidance includes package installation and compilation commands that may change a user's local TeX environment or build output. <br>
Mitigation: Run any tlmgr or LaTeX compilation command yourself in the intended project environment and inspect the generated PDF before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bg1avd/latex-verbatim-center) <br>
- [README.md](README.md) <br>
- [QUICKREF.md](QUICKREF.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with LaTeX snippets and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a global verbatim redefinition that users should review before applying.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
