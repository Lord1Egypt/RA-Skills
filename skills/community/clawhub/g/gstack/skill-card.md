## Description:

Gstack provides Claude Code workflow skills for planning, review, shipping, QA, release documentation, retrospectives, and fast headless browser dogfooding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ovyeddeno](https://clawhub.ai/user/ovyeddeno)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering leads, and QA engineers use Gstack to invoke focused Claude Code workflows for product planning, architecture review, code review, release execution, browser-based QA, bug fixing, and release documentation. It is intended for users who want repeatable specialist agent behavior while building and validating software.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access authenticated browser sessions and persist local browser state or logs.

Mitigation: Install only in trusted environments, avoid importing production cookies, and clear local session state when sensitive testing is complete.

Risk: Setup and upgrade flows can run commands and fetch or update local skill code.

Mitigation: Review the exact setup or upgrade commands before execution, keep auto-upgrade disabled unless the upstream source is trusted, and verify changes before continuing work.

Risk: Project instruction changes can alter future agent behavior.

Mitigation: Review any CLAUDE.md or project instruction edits before accepting them.

## Reference(s):

- [ClawHub Gstack Skill Page](https://clawhub.ai/ovyeddeno/skills/gstack)
- [ClawHub Publisher Profile](https://clawhub.ai/user/ovyeddeno)
- [QA Issue Taxonomy](qa/references/issue-taxonomy.md)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Playwright](https://playwright.dev/)
- [Bun](https://bun.sh/)
- [Conductor](https://conductor.build)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, code edits, configuration steps, QA reports, review findings, and release notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or modify project files, run local shell commands, operate a persistent headless browser session, and write local browser state or logs depending on the invoked workflow.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata, created 2026-03-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
