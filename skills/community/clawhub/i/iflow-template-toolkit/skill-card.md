## Description: <br>
Dependency-free template engine with variable substitution, conditionals, loops, and multi-language support for iFlow skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sylvanxiao](https://clawhub.ai/user/sylvanxiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building iFlow skills use this toolkit to render text, Markdown, code, or configuration from simple templates and to add lightweight English and Chinese localization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendering untrusted template filenames or template text can produce misleading output or expose data supplied in the render context. <br>
Mitigation: Use trusted templates, review rendered output before applying it, and pass plain dictionaries rather than sensitive objects as template context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sylvanxiao/iflow-template-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration] <br>
**Output Format:** [Rendered template text and localized strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dependency-free Python helper; template rendering uses caller-provided templates and context dictionaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
