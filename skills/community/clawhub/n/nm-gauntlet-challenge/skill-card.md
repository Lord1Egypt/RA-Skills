## Description: <br>
Presents adaptive codebase challenge questions with multiple-choice and trace exercises. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to run adaptive codebase knowledge challenges, present multiple-choice or trace questions, evaluate responses, and update local Gauntlet progress state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local .gauntlet files can contain challenge history, knowledge entries, progress, and pending challenge state that may be sensitive in some repositories. <br>
Mitigation: Review the .gauntlet files before and after use, and run the skill only in repositories where updating local challenge state is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-gauntlet-challenge) <br>
- [Gauntlet plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown challenge prompts, answer evaluations, scoring summaries, and occasional Python setup snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local .gauntlet knowledge, pending challenge, progress, and pass-token state files.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
