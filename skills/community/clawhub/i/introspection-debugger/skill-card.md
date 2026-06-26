## Description: <br>
AI Agent 自省调试框架 helps agents capture runtime errors, analyze likely root causes, attempt automatic repairs, and generate structured introspection reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danihe001](https://clawhub.ai/user/danihe001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add self-diagnosis, repair attempts, error history, and human escalation to JavaScript-based agent workflows. It is most useful when an agent needs structured reporting for failures such as missing files, permissions, missing modules, timeouts, rate limits, server errors, memory issues, and authentication failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic repair behavior can modify the workspace by creating files, changing permissions, or installing npm packages. <br>
Mitigation: Install only in a disposable or tightly scoped workspace, and require explicit review before enabling automatic file creation, chmod, or npm install behavior. <br>
Risk: Detailed error reports can be sent to an external notification hook. <br>
Mitigation: Use notification hooks only after confirming reports are redacted and safe to share outside the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danihe001/introspection-debugger) <br>
- [Publisher profile](https://clawhub.ai/user/danihe001) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown usage guidance with JavaScript code examples; runtime output is structured report data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit error and report events and can call a configured notification hook.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
