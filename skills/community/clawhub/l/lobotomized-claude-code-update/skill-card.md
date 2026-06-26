## Description: <br>
Gated two-stage upgrade of a lobotomized Claude Code stack - the CC binary, skrabe/lobotomized-claude-code overrides, and the skrabe/tweakcc-fixed patcher. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers who intentionally use the third-party LCC/tweakcc Claude Code override stack can use this skill to check for supported updates, review the proposed changes, and apply the upgrade after explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally updates a local Claude Code installation and prompt-override stack, which can change local agent behavior. <br>
Mitigation: Install only when this stack is expected, review the Stage 1 report, and approve Stage 2 only after checking repo origins, target versions, local changes, and blockers. <br>
Risk: A stale patcher cache can apply old-version content to a new Claude Code binary. <br>
Mitigation: Clear the stale apply cache before re-applying overrides during a version change. <br>
Risk: Local repository divergence or tracked file edits can make an automated upgrade unsafe. <br>
Mitigation: Use the pre-flight blocker checks and fast-forward-only pulls; stop for a human decision when local-only commits or tracked edits are present. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/tenequm/lobotomized-claude-code-update) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/tenequm) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown report with inline shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stage 1 is read-only and stops for approval before Stage 2 applies updates.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
