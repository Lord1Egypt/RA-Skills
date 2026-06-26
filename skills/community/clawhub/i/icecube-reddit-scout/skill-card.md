## Description: <br>
IceCube Reddit Scout helps agents monitor Reddit keywords, collect mention context, and surface leads, product ideas, competitor mentions, and trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ares521521-design](https://clawhub.ai/user/ares521521-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up an agent-assisted Reddit monitoring workflow for brand monitoring, lead discovery, idea validation, competitor tracking, and trend detection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use Reddit OAuth, a logged-in browser, or Reddit alert emails, which can expose sensitive account, inbox, or session data. <br>
Mitigation: Use a dedicated Reddit app or token and a dedicated email label or mailbox with the minimum access needed. <br>
Risk: Mention logs can persist Reddit content, lead data, and outreach context locally. <br>
Mitigation: Avoid storing raw email bodies or full comment text, and review or delete memory logs on a regular schedule. <br>
Risk: Automated lead generation or reply drafting can produce unwanted outreach or policy-sensitive activity. <br>
Mitigation: Require human approval before posting replies, sending outreach, or acting on generated leads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ares521521-design/icecube-reddit-scout) <br>
- [Reddit app preferences](https://www.reddit.com/prefs/apps) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce local mention logs and proposed outreach drafts that should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
