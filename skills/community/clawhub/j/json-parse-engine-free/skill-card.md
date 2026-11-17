## Description: <br>
Json Parse Engine Free helps agents parse JSON from files or strings, flatten nested structures, extract values by dotted paths, validate required fields, and report parse errors and record counts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, operations engineers, and testing teams use this skill to turn nested JSON into easier-to-consume structures for preprocessing, reporting, configuration inspection, log analysis, and field completeness checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests local read, write, and command-execution access even though the described JSON parsing workflow does not clearly require write access. <br>
Mitigation: Run it only in trusted workspaces, limit inputs to user-selected JSON files, avoid files containing secrets, and treat write access as unnecessary unless the publisher documents bounded output-saving behavior. <br>
Risk: The free edition describes full-file parsing and warns that large files can exceed memory limits. <br>
Mitigation: Use small or pre-split JSON files, avoid directory-level or bulk processing, and review generated commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/json-parse-engine-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and JSON-shaped result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns success, data, execution_log, and error fields; the free edition describes a 10 MB single-file limit and no streaming or batch parsing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
