## Description: <br>
This skill guides agents through converting YAML files to JSON and JSON files to YAML with the jyml CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waldekmastykarz](https://clawhub.ai/user/waldekmastykarz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert configuration, OpenAPI, GitHub Actions, and API response files between YAML and JSON formats. It also helps agents produce shell commands for one-off, custom-output, indented, structured, and batch conversions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs users to install or run an external npm package. <br>
Mitigation: Use npx for one-off conversions or verify the package source before installing jyml globally. <br>
Risk: Default conversion writes a new file next to the input, and custom output paths can write elsewhere. <br>
Mitigation: Review input and output paths before conversion and use explicit output paths when overwrites or directory changes matter. <br>
Risk: Invalid or unexpected YAML or JSON input can cause conversion errors or produce unexpected structured output. <br>
Mitigation: Confirm file extensions and syntax before conversion, and inspect structured JSON output before piping it into other tools. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/waldekmastykarz/jyml) <br>
- [Publisher profile](https://clawhub.ai/user/waldekmastykarz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline jyml, npx, npm, jq, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe file outputs written next to the input file or to a custom output path; structured mode can emit JSON to stdout.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
