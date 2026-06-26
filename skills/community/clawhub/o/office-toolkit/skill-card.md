## Description: <br>
A document-processing toolkit for Microsoft Office documents and PDF files that supports reading, writing, format conversion, and batch-oriented workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weiwei2027](https://clawhub.ai/user/weiwei2027) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document automation users use this skill to inspect, create, and convert DOCX, PPTX, XLSX, and PDF files from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted Office, PDF, XML, or image files may expose parser vulnerabilities in document-processing dependencies. <br>
Mitigation: Process untrusted documents in an isolated virtual environment and keep parser dependencies pinned, locked, and updated. <br>
Risk: The skill reads and writes local document files, so an agent may modify or create files when invoking the bundled scripts. <br>
Mitigation: Review target paths before execution and run the skill with least-privilege filesystem access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weiwei2027/office-toolkit) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, plus plain text or JSON output from document-processing scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated or modified Office/PDF files may be produced when the agent runs the bundled scripts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
