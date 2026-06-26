## Description: <br>
Parses and converts log lines into JSON for easier analysis, debugging, and forwarding to log aggregation tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert log files or piped log streams into line-delimited JSON for inspection, debugging, and downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Processed logs may contain sensitive data and the default output preserves the original log line. <br>
Mitigation: Review logs before processing highly sensitive data and use --no-log-field when the original line should not be retained. <br>
Risk: The advertised logfmt_parser wrapper may not be installed in every agent runtime. <br>
Mitigation: Invoke the bundled tool.py directly when no wrapper command is available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/logfmt-parser) <br>
- [Publisher profile](https://clawhub.ai/user/albionaiinc-del) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-oriented output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The parser emits one JSON object per processed log line and can optionally extract timestamps or omit the original log field.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
