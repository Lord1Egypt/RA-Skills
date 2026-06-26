## Description: <br>
Lint Markdown files for formatting issues, broken links, and style consistency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Derick001](https://clawhub.ai/user/Derick001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation maintainers, and agents use this skill to scan Markdown files for formatting, style, and link issues before publication or release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional external link checking may contact URLs embedded in Markdown files from the user's environment. <br>
Mitigation: Keep external link checking disabled unless network validation is intentional, especially for private or third-party Markdown files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Derick001/markdown-linter-cli) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [JSON lint results with issue locations, severities, messages, suggested fixes, and summary counts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can process one or more Markdown files from comma-separated paths or glob patterns; external link checks are optional.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
