## Description: <br>
macOS 只读查询：Mail 未读、Calendar 日程、Notes 搜索、Stocks 行情（输出 JSON）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lilei0311](https://clawhub.ai/user/lilei0311) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill on macOS to query unread Mail messages, Calendar events, Notes folders and note search results, and stock quotes as structured JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can return private Mail subjects and senders, Calendar details, and Notes snippets once macOS permissions are granted. <br>
Mitigation: Grant permissions only in environments where the agent is allowed to inspect that personal data, and review returned JSON before sharing it outside the local workflow. <br>
Risk: Stock quote commands contact qt.gtimg.cn with requested symbols. <br>
Mitigation: Use stock quote commands only when external quote lookups are acceptable for the symbols being requested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lilei0311/macos-suite-readonly) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/lilei0311) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each command writes a single JSON object with ok/action status and command-specific result fields.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
