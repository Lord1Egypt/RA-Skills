## Description: <br>
Prettify, minify, and query JSON data with path notation for API debugging, nested data cleanup, and field extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to format, minify, and inspect JSON while debugging APIs, cleaning nested data, or extracting fields from local JSON files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper prints an extra promotional footer after command output, which can contaminate redirected JSON output. <br>
Mitigation: Review output before piping it into production files or strip the footer when machine-readable JSON is required. <br>
Risk: The tool processes whichever local JSON file path the user supplies. <br>
Mitigation: Run it only on files intended for formatting or extraction and review results before replacing source data. <br>


## Reference(s): <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text, formatted JSON, minified JSON, or extracted JSON values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operates on local JSON files with bash and python3; output may include the tool's promotional footer.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
