## Description:

Goal Setter helps agents manage local personal goals, milestones, progress updates, reviews, and simple motivation prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal productivity agents use this skill to create, update, review, and archive goals in local JSON storage without external accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted goal names, milestones, deadlines, or progress values can cause unintended local Python code execution.

Mitigation: Do not use this skill with untrusted text or automated inputs until the command script passes user values to Python as data rather than source code.

Risk: Goal data is stored locally under $HOME/.goals by default.

Mitigation: Review local storage expectations before use and set GOAL_DIR when goals should be isolated to a specific directory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain1/skills/goal-setter)
- [Tips for Goal Setter](tips.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local goal data stored under $HOME/.goals by default.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
