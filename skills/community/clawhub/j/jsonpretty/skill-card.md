## Description: <br>
Format, validate, query, flatten, and analyze JSON data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rogue-agent1](https://clawhub.ai/user/rogue-agent1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect JSON from files or stdin, including pretty-printing, syntax validation, dot-notation queries, flattened key-value output, compact output, sorted keys, and structure statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: JSON content supplied to the tool may include secrets or sensitive data that are printed to the terminal or captured in logs. <br>
Mitigation: Avoid running the skill on secrets unless terminal output and logging are acceptable for that data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rogue-agent1/jsonpretty) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text, JSON, and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads JSON from a file path or stdin and writes formatted output, validation messages, query results, flattened values, or statistics to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
