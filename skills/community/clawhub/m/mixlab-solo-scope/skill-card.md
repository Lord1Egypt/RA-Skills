## Description: <br>
Fetches entries from the Solo Scope RSS feed, organizes them into 3-6 concise topic groups, writes a short core-value summary for each group, and returns a Markdown briefing with original titles and links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shadowcz007](https://clawhub.ai/user/shadowcz007) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and operators use this skill to turn the Solo Scope RSS feed into an actionable daily Markdown briefing for solo founders and small teams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts an external MixDAO RSS feed during normal use. <br>
Mitigation: Install and run it only in environments where outbound access to that feed is acceptable. <br>
Risk: RSS entries may contain external links or content that changes after the briefing is generated. <br>
Mitigation: Review generated links and source items before opening links or acting on the briefing. <br>
Risk: Writing the report to a project file may leave external-feed content in the workspace. <br>
Mitigation: Prefer direct chat output unless a persisted project file is specifically needed. <br>


## Reference(s): <br>
- [Solo Scope RSS feed](https://www.mixdao.world/feed) <br>
- [ClawHub skill listing](https://clawhub.ai/shadowcz007/mixlab-solo-scope) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown briefing with grouped links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Groups RSS items into 3-6 categories and keeps each category summary within 140 Chinese characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
