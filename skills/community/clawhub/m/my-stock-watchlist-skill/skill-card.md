## Description: <br>
Manages a stock watchlist stored in a DingTalk multidimensional table when the user asks about an observation list or stock watchlist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canonxu](https://clawhub.ai/user/canonxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users managing a stock watchlist use this skill to add, remove, and query ticker symbols in a specified DingTalk table. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add or delete rows in the specified DingTalk stock watchlist. <br>
Mitigation: Use least-privileged DingTalk access and require confirmation before deletions when accidental removal would matter. <br>
Risk: The skill depends on a fixed DingTalk table, sheet, and stock-code field mapping. <br>
Mitigation: Verify the table ID, sheet ID, and `标的` field before using the skill in a live watchlist. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/canonxu/my-stock-watchlist-skill) <br>
- [DingTalk Stock Watchlist Table](https://alidocs.dingtalk.com/i/nodes/1OQX0akWmxpyBpnaCQQQoYkY8GlDd3mE) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Guidance] <br>
**Output Format:** [Plain text or Markdown responses backed by DingTalk table API actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the dingtalk-ai-table dependency to add, delete, read, and summarize watchlist records.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact skill.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
