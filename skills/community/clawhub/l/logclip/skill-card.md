## Description: <br>
Logclip extracts and reformats timestamped log entries from text within a specified date range using custom patterns and output formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Logclip to isolate relevant events from raw or mixed log text, filter them by date range, and normalize timestamp output for review or handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input logs or filtered output may contain secrets or sensitive operational data. <br>
Mitigation: Review logs before processing or sharing output, and keep filtered results within the intended local environment. <br>
Risk: The documentation examples invoke logclip.py, while the released artifact contains tool.py. <br>
Mitigation: Run the bundled tool.py file directly unless it is intentionally renamed in the local environment. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/albionaiinc-del/logclip) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with bash examples and plain-text filtered log output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts stdin or file input, start and end datetimes, an optional timestamp format, and an optional custom timestamp regex.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
