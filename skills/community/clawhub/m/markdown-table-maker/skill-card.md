## Description: <br>
Create, format, align, sort, transpose, and convert Markdown tables from CSV or JSON using a zero-dependency Python helper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darbling](https://clawhub.ai/user/darbling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to generate GitHub-Flavored Markdown tables, convert simple CSV or JSON data into tables, and reformat existing Markdown tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Output options write to the local path supplied by the user. <br>
Mitigation: Review input and output file paths before running the script and write only to intended project locations. <br>
Risk: The documentation overstates TSV and merge support in this version. <br>
Mitigation: Confirm supported commands with the bundled script help and use the implemented create, from-csv, from-json, align, sort, and transpose commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/darbling/markdown-table-maker) <br>
- [Declared GitHub repository](https://github.com/darbling/clawhub-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables with optional plain-text command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write generated tables to user-specified local output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
