## Description:

Generates or updates tutorials from VHS tapes and Playwright specs with dual-tone markdown and GIF recording.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create or refresh user-facing tutorials from terminal tapes and browser specs, including demo recordings and documentation for project docs and a technical book.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious and reports incomplete analysis, including behaviors beyond the stated tutorial-generation purpose.

Mitigation: Review the skill and the partially analyzed validation material before installing, and decide whether the reported behavior is acceptable.

Risk: Tape commands run with the user's permissions, and a rebuild can affect normally installed Cargo commands.

Mitigation: Inspect tape commands and rebuild targets before execution; use a disposable workspace and toolchain where practical.

Risk: Terminal or browser recordings may capture sensitive information.

Mitigation: Use sanitized demo data and review recordings before sharing or publishing them.

## Reference(s):

- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-sanctum-tutorial-updates)

## Skill Output:

**Output Type(s):** [Markdown, Files, GIF images]

**Output Format:** [Markdown tutorial files and GIF recordings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update tutorial assets and README demo sections; produces brief project docs and detailed book documentation.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
