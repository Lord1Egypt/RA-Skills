## Description: <br>
Search, summarize, and extract insights from your Limitless AI pendant life logs. Supports keyword and semantic search, date range queries, memory recall, and action item extraction for named agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeremytoce](https://clawhub.ai/user/jeremytoce) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and external users with Limitless AI pendant recordings use this skill to search lifelog transcripts, summarize recent activity, recall decisions, browse date ranges, and extract agent-directed action items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive Limitless transcript content. <br>
Mitigation: Install only if transcript access is intended, and review or redact quoted transcript content before sharing it outside the local workflow. <br>
Risk: Dispatch can send transcript-derived quotes and metadata to configured webhooks or email recipients. <br>
Mitigation: Inspect every configured dispatch URL or recipient and approve sends only after confirming the destination and payload. <br>
Risk: The security guidance notes that the agent roster path should be fixed or verified before dispatch use. <br>
Mitigation: Verify the agents.json location and contents before relying on action item detection or dispatch behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeremytoce/limitless-lifelogs) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jeremytoce) <br>
- [Limitless API base URL](https://api.limitless.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, excerpts, structured action items, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transcript-derived quotes, log IDs, timestamps, and dispatch payload details after user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
