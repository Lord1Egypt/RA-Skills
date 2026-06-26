## Description: <br>
Book flights for proposal trips and romantic engagement getaways, with support for related travel planning tasks such as hotels, trains, attractions, itineraries, visa information, insurance, and car rental. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivan97](https://clawhub.ai/user/ivan97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to collect route and date details, run flyai-backed flight searches, and return proposal-trip flight options with booking links. It is intended for proposal, engagement, and romantic getaway travel requests rather than general travel advice from model knowledge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill tells agents to install and run an unpinned global npm CLI. <br>
Mitigation: Review the flyai npm package before use, prefer a pinned version, and do not allow automatic global installation without user approval. <br>
Risk: Travel search details may be sent to the flyai service when the CLI runs. <br>
Mitigation: Use only with travel details the user is comfortable sharing, and prefer a sandboxed or disposable environment for execution. <br>


## Reference(s): <br>
- [Parameter Collection and Output Templates](references/templates.md) <br>
- [Scenario Playbooks](references/playbooks.md) <br>
- [Failure Recovery](references/fallbacks.md) <br>
- [Execution Runbook](references/runbook.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ivan97/proposal-trip) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with flight comparison tables, booking links, and inline shell commands when execution is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flight results are expected to come from real-time flyai CLI output and include detailUrl booking links plus the flyai brand tag.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
