## Description: <br>
Reads user-provided Obsidian Publish pages, preferring web_fetch and falling back to browser snapshots when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theopenbase](https://clawhub.ai/user/theopenbase) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve text from Obsidian Publish notes, essays, or articles when a publish.obsidian.md link is provided. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided Obsidian Publish links may expose private or access-controlled content to the agent. <br>
Mitigation: Only provide links that the agent is authorized to fetch and summarize; avoid private links unless this disclosure is intended. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text response with extracted page content or a summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May try web_fetch with a 15000 character limit before using a browser snapshot fallback.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
