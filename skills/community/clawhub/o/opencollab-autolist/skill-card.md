## Description: <br>
Automatically registers or updates an OpenCollab freelancing profile, posts skill listings, checks job matches, scores opportunities, and drafts or submits proposals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssidharhubble](https://clawhub.ai/user/ssidharhubble) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and freelance operators use this skill to manage an OpenCollab marketplace presence, list high-demand technical services, monitor matching jobs, and track proposal activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs an agent to act on a live freelance marketplace, including account creation, profile edits, listings, and public proposals. <br>
Mitigation: Use explicit per-action confirmation and set clear limits for account creation, profile changes, listings, proposal volume, scheduling, and credential storage. <br>
Risk: The skill tells the agent to find current OpenCollab API endpoints and authentication details, which could lead to unreliable or unsafe integration behavior. <br>
Mitigation: Use only official OpenCollab API documentation and user-provided limited-scope credentials before making marketplace changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ssidharhubble/opencollab-autolist) <br>
- [Publisher profile](https://clawhub.ai/user/ssidharhubble) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with operational steps and status-style outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include profile URLs, listing counts, job counts, proposal counts, and win-rate tracking.] <br>

## Skill Version(s): <br>
1.0.18 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
