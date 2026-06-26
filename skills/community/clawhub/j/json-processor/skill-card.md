## Description: <br>
JSON query, validate, diff, transform, format, flatten, and stats toolkit with a jq-like interface using only the Python standard library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlooi504](https://clawhub.ai/user/ericlooi504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect, validate, compare, transform, format, flatten, and summarize JSON data during local engineering workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read JSON files that may contain secrets or private data. <br>
Mitigation: Use it only with files the agent is allowed to inspect, and avoid passing sensitive JSON unless that access is intended. <br>
Risk: Formatting and flattening commands can write to user-specified output paths. <br>
Mitigation: Review output paths before execution to avoid overwriting files unintentionally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ericlooi504/json-processor) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [json_processor.py](artifact/scripts/json_processor.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python CLI commands and JSON/text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can read JSON from files or stdin and can write formatted or flattened JSON to user-specified output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
