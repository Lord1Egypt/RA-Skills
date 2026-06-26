## Description: <br>
A Chinese writing assistant skill that helps agents research recent context and rewrite drafts into more natural, platform-specific human-facing prose. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengpengliu1212-art](https://clawhub.ai/user/pengpengliu1212-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and content teams use this skill to turn a topic or AI draft into Chinese social-platform copy for Xiaohongshu, Douyin, WeChat, or Weibo. The skill guides the agent to confirm a time window, research recent background, ask for platform and narrative perspective, and produce a more conversational final draft. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use web search for current topics, which may expose sensitive draft themes or confidential topics if the user includes them in queries. <br>
Mitigation: Avoid confidential drafts or sensitive topics in searches, and use the skill only with material appropriate for web-assisted research. <br>
Risk: The skill records writing-style preferences in persistent memory, which can retain user-specific style information across sessions. <br>
Mitigation: Review or delete /workspace/memory/evolution/user-writing-style.md periodically, and ask the agent not to update memory for one-off rewrites. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pengpengliu1212-art/humanize-write) <br>
- [Publisher profile](https://clawhub.ai/user/pengpengliu1212-art) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown and Chinese prose] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include platform label, draft body, creation date, selected style, narrative perspective, and background summary.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and artifact text) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
