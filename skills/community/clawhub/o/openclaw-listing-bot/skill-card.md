## Description: <br>
Autonomous agent that creates, smoke-tests, lists, tracks, and deprecates marketplace skill listings on a recurring loop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssidharhubble](https://clawhub.ai/user/ssidharhubble) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketplace operators and developers use this skill to automate creating and publishing agent skill listings based on demand and earnings signals. It is intended for users who deliberately want autonomous marketplace listing activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad unattended authority to create, publish, and retire marketplace listings. <br>
Mitigation: Require manual review before every publish or deprecation action, and avoid running it as a background loop until approval controls exist. <br>
Risk: Generated listings or files may include secrets, unreviewed content, or unintended workspace material. <br>
Mitigation: Use a dedicated staging directory and scan all generated or selected files before any marketplace sync. <br>
Risk: Automated deprecation based on traction metrics can remove listings without appropriate oversight. <br>
Mitigation: Require explicit human approval for retirement actions and retain logs for each decision. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/ssidharhubble/openclaw-listing-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown skill files, shell commands, JSON logs, and marketplace listing content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed to run as an iterative publishing loop; review generated files and actions before publishing or deprecating listings.] <br>

## Skill Version(s): <br>
1.0.18 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
