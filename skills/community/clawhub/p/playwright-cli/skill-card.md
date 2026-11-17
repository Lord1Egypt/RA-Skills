## Description:

A Playwright CLI browser automation skill for web testing, page interaction, E2E workflows, multi-session automation, screenshots, PDF export, network routing, and spec-driven test generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to drive browser automation through Playwright CLI commands, inspect pages, manage sessions and storage, debug web behavior, and generate or maintain Playwright E2E tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad browser automation can expose logged-in sessions, cookies, tokens, or saved auth state.

Mitigation: Use isolated test accounts and browser profiles, avoid attaching to a personal logged-in browser, and protect or delete any exported cookies, tokens, or auth state.

Risk: Running npm or npx commands can execute mutable package versions or unexpected package code.

Mitigation: Pin package versions and install only in trusted workspaces where the package source and lockfiles can be reviewed.

Risk: The run-code flow can execute arbitrary Playwright or JavaScript code in a browser context.

Mitigation: Do not run untrusted scripts, and review custom code before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/playwright-cli)
- [Playwright documentation](https://playwright.dev)
- [Command reference](references/commands.md)
- [Usage examples](references/examples.md)
- [Spec-driven testing](references/spec-testing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Playwright TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots, PDFs, videos, trace files, YAML snapshots, JSON output, and browser state files when the referenced CLI commands are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
