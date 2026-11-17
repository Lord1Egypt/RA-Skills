## Description: <br>
Json Beautifier Free helps agents format, minify, validate, and extract JSONPath paths from small JSON inputs for development and debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, analysts, and testers use this skill to clean up JSON for API debugging, configuration review, log inspection, and JSONPath extraction. It is intended for lightweight local processing of small JSON inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill declares broader write and shell execution access than basic JSON formatting usually needs. <br>
Mitigation: Grant only read access by default, enable shell or write access only for a specific local workflow, and review any proposed command before execution. <br>
Risk: Malformed or untrusted JSON could produce incorrect results or encourage writing unsafe output files. <br>
Mitigation: Validate JSON before downstream use, keep processing local, and prefer chat responses unless an output file is explicitly requested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/json-beautifier-free) <br>
- [Publisher homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [Text or JSON responses containing formatted JSON, minified JSON, validation results, JSONPath lists, status details, and logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports options such as indentation width, key sorting, Unicode escaping, compact output, and JSON/text/CSV-style result presentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
