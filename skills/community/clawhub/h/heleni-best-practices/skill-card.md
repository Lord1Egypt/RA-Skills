## Description: <br>
Daily check of Heleni's PA Skills website for new best practices, lessons learned, and skill updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent owners use this skill to check Heleni's PA Skills site for new lessons, skill updates, and best-practice changes that may inform an agent's own setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mutable external content can influence persistent agent behavior. <br>
Mitigation: Require visible diffs and explicit approval before changing SOUL.md, AGENTS.md, HOT.md, skill descriptions, installed skills, or other persistent behavior. <br>
Risk: Daily scheduled checks fetch and evaluate remote Heleni PA Skills content. <br>
Mitigation: Install only when the publisher and Heleni PA Skills source are trusted, and review fetched updates before applying them. <br>


## Reference(s): <br>
- [Heleni PA Skills](https://netanel-abergel.github.io/pa-skills/) <br>
- [Heleni PA Skills Lessons](https://netanel-abergel.github.io/pa-skills/learn.html) <br>
- [Heleni PA Skills About](https://netanel-abergel.github.io/pa-skills/about.html) <br>
- [Heleni PA Skills GitHub Repository](https://github.com/netanel-abergel/pa-skills) <br>
- [ClawHub Skill Page](https://clawhub.ai/netanel-abergel/heleni-best-practices) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local state JSON file and markdown learning logs when run by an agent.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
