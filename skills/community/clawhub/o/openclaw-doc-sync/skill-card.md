## Description: <br>
Post-release documentation sync skill that aligns README, ARCHITECTURE, CONTRIBUTING, and CLAUDE.md with actual changes, cleans up TODOs, polishes changelog tone, and can optionally update version metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill after implementation work and before release or merge to synchronize repository documentation, TODOs, changelog wording, and version decisions with the actual diff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill updates repository documentation and can create a local docs commit, which may introduce incorrect documentation if the resulting diff is not reviewed. <br>
Mitigation: Run it on a feature branch and review the resulting diff and commit before pushing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/x-rayluan/openclaw-doc-sync) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and repository documentation edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask the user before risky narrative changes, new TODOs, or version updates; otherwise applies clear factual documentation updates.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
