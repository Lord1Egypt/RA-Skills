## Description: <br>
Analyzes Oracle PL/SQL package files for a requested stored procedure, mapping upstream and downstream procedure dependencies, data flow, exact line references, mechanism details, and the procedure body. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JohnsRun](https://clawhub.ai/user/JohnsRun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use this skill to inspect Oracle PL/SQL packages, trace stored procedure callers and callees, and produce reviewable Markdown analysis with exact source-line links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads user-provided PL/SQL package files, which may contain proprietary schema or business logic. <br>
Mitigation: Use it only with package files approved for the agent workspace and avoid attaching sensitive database code unless that access is acceptable. <br>
Risk: Generated dependency chains, table reads, and line references may be incomplete or incorrect if the package is complex or the attached file is not the exact source version. <br>
Mitigation: Review the Markdown analysis, dependency lists, and clickable line references against the source package before relying on the output. <br>


## Reference(s): <br>
- [Example output](artifact/examples/examples_output.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analysis with headings, bullets, inline code, source links, and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes upstream and downstream procedure sections, mechanism analysis, and target procedure body script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
