## Description: <br>
Format and validate JSON files with pretty-printing, indentation control, key sorting, and validation modes supporting stdin, stdout, and file I/O. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to format, validate, and normalize JSON from files or stdin before using it in configuration, API debugging, or data review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool reads JSON files or stdin supplied by the user, which may expose sensitive data to a local third-party skill. <br>
Mitigation: Run it only on JSON content you are comfortable processing with this publisher's local tool, and avoid sensitive files unless the publisher is trusted. <br>
Risk: The output option writes to a user-selected path and could overwrite an important file. <br>
Mitigation: Review the destination path before execution and write to a new or temporary file when preserving the original matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/json-formatter-pro) <br>
- [Publisher profile](https://clawhub.ai/user/harrylabsj) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands] <br>
**Output Format:** [Markdown guidance with shell command examples and formatted JSON or validation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads JSON from stdin or selected files and can write formatted output to stdout or a user-selected output path.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
