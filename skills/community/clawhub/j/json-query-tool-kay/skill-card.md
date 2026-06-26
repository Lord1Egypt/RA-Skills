## Description: <br>
JSON Query Tool helps agents extract and format values from JSON files using simple path expressions without extra dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect API responses, configuration files, and JSON-style logs by extracting fields or formatting results as raw text, JSON, or tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool reads local JSON files and may surface sensitive values if pointed at secrets, credentials, or raw API responses. <br>
Mitigation: Run it only on intended files and redact credentials or personal data before sharing output. <br>
Risk: Missing paths and invalid inputs can produce null results or nonzero exits that downstream scripts may mishandle. <br>
Mitigation: Check command exit status and validate extracted output before using it in automation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, Tables, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, plus raw text, JSON, or table output from the JSON query tool.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local JSON files and supports dot paths, array indexes, wildcards, and raw/json/table output formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
