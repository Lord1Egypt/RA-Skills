## Description:

Systematically improve code through disciplined analysis, targeted mutations, verification, scoring, and logging to iteratively enhance quality and design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronjmars](https://clawhub.ai/user/aaronjmars)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill when code, prompts, pipelines, or agent workflows need disciplined multi-cycle improvement rather than one-shot edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Evolution logs and archived variants can contain sensitive implementation details, credentials, production data, or failure notes if the agent records them during iterative work.

Mitigation: Use the skill only in repositories where local experiment logs are acceptable, add `.evolution/` to `.gitignore` for private work, review log contents before sharing, and keep secrets out of archived notes and variants.

## Reference(s):

- [ALMA research framework](https://yimingxiong.me/alma)
- [ClawHub skill page](https://clawhub.ai/aaronjmars/skills/iterative-code-evolution)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with code, shell-command, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local .evolution/ logs and variant files during iterative work.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
