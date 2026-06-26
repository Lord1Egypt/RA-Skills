## Description: <br>
Generates low-code module scaffolding for backend Java services, React frontend pages, SQL initialization, and related module configuration from a Chinese module name and field definition table. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hjfeilg](https://clawhub.ai/user/hjfeilg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create consistent backend, frontend, and database scaffolding for new low-code platform modules. It is intended for module generation workflows where the user supplies a Simplified Chinese module name, field definitions, and optional layout or relation details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated backend, frontend, and SQL files may be written to unintended project paths if output locations are wrong or omitted. <br>
Mitigation: Confirm the backend, frontend, and SQL output paths in src/config.json or provide explicit paths before using the generated artifacts. <br>
Risk: Generated code or init.sql may not match the intended module structure when layout keywords, relation settings, or Chinese text conversion are ambiguous. <br>
Mitigation: Review generated code and init.sql before committing or applying them, especially for layout choices and relation fields. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hjfeilg/lowcode-module-generator) <br>
- [Publisher profile](https://clawhub.ai/user/hjfeilg) <br>


## Skill Output: <br>
**Output Type(s):** [code, markdown, configuration, guidance] <br>
**Output Format:** [Markdown and generated source-code snippets or files for Java, React, mapper XML, SQL, and module configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated output depends on the target backend, frontend, and SQL paths plus the module fields and layout choices supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
