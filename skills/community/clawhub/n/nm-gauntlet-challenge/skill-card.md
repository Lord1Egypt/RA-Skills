## Description: <br>
Presents adaptive codebase challenge questions with multiple-choice and trace exercises. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to test contributor knowledge of a codebase through adaptive questions, answer evaluation, scoring, and progress tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read and update local .gauntlet state files while evaluating challenges. <br>
Mitigation: Review proposed file access and state changes, and grant access only inside the intended repository challenge workflow. <br>
Risk: Challenge scoring and explanations can be incomplete or inaccurate for a contributor's actual codebase knowledge. <br>
Mitigation: Use scoring as workflow guidance and review important pass, partial, or fail outcomes before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-gauntlet-challenge) <br>
- [Gauntlet homepage](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, files] <br>
**Output Format:** [Markdown challenge prompts, scoring feedback, explanations, and local state-file updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update .gauntlet knowledge, pending challenge, progress, and pass-token state when used in a gauntlet workflow.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
