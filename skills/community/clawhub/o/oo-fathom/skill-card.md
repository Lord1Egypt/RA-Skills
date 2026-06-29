## Description: <br>
Operates Fathom Analytics through an OOMOL-connected account for reading analytics data and creating or updating sites, events, milestones, and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect Fathom Analytics account, site, event, milestone, visitor, and aggregation data, and to make confirmed updates when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update Fathom Analytics sites, events, and milestones. <br>
Mitigation: Require user confirmation of the exact action payload and expected effect before running any write action. <br>
Risk: The OOMOL connection gives the agent account-level access to Fathom Analytics data available to the connected API key. <br>
Mitigation: Install only when this access is intended, keep the OOMOL connection scoped to the intended account, and review proposed actions before approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-fathom) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Fathom Analytics homepage](https://usefathom.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Fathom connector JSON responses when actions are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
