## Description: <br>
Parse JSON, CSV, XML, and logs into structured output for format conversion, structure validation, field extraction, and nested data analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and data-focused agents use this skill to parse local JSON, CSV, XML, YAML, text, and log files, extract fields or patterns, and summarize file structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill parses local files and may print sensitive file contents or extracted values into the agent conversation. <br>
Mitigation: Use it only on files intended for analysis, and avoid supplying secrets or sensitive datasets unless that exposure is expected. <br>
Risk: Parse results can be cached under the user's local data directory. <br>
Mitigation: Review or clear the parser cache when working with sensitive input files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/parser) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, structured text tables, JSON, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the selected parser command and the supplied local file.] <br>

## Skill Version(s): <br>
3.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
