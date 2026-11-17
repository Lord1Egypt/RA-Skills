## Description:

Lightweight PIV workflow - discovery-driven feature builder. No PRD needed. Asks quick questions, generates PRP, executes with validation loop. For small-to-medium features when you want to skip PRD ceremony.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smokealot420](https://clawhub.ai/user/smokealot420)

### License/Terms of Use:


## Use Case:

Developers use this skill to turn a small-to-medium feature idea into a PRP, execute implementation, validate results, debug gaps, and optionally prepare a commit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run project commands and make broad repository changes.

Mitigation: Use it only in a clean, disposable or well-sandboxed repository and review generated PRPs, proposed commands, and changed files before allowing execution to continue.

Risk: The Smart Commit step can stage broad changes and add unwanted promotional text to the commit message.

Mitigation: Do not allow the commit step until the exact staged files and commit message have been reviewed and any forced promotional text has been removed.

Risk: Repository commands may expose secrets or operate on sensitive local state.

Mitigation: Keep secrets out of the environment used for this skill and run it in an isolated working copy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smokealot420/skills/mini-piv)
- [Project homepage](https://github.com/SmokeAlot420/ftw)
- [Codebase analysis workflow](references/codebase-analysis.md)
- [PRP generation workflow](references/generate-prp.md)
- [PRP execution workflow](references/execute-prp.md)
- [PIV executor role](references/piv-executor.md)
- [PIV validator role](references/piv-validator.md)
- [PIV debugger role](references/piv-debugger.md)
- [Base PRP template](assets/prp_base.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, PRPs, execution summaries, validation reports, code changes, and shell command suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires git and is marked for darwin and linux environments in ClawHub metadata.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
