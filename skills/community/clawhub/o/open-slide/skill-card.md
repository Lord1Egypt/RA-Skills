## Description:

Create, edit, preview, and export web-native slide decks with the open-slide React framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[windrichie](https://clawhub.ai/user/windrichie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to scaffold, author, edit, preview, and export React-based slide decks with open-slide.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation can pull unpinned third-party npm and Python packages.

Mitigation: Install in an isolated development environment and review or pin npm and Python dependency versions when reproducibility matters.

Risk: The scaffold and export workflow runs local Node.js, Python, Playwright, and Chromium tooling.

Mitigation: Run the workflow from a normal development account without sensitive production credentials.

## Reference(s):

- [Open Slide ClawHub page](https://clawhub.ai/windrichie/skills/open-slide)
- [Open-slide upstream framework](https://github.com/1weiho/open-slide)
- [Slide authoring reference](references/authoring.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and React/TypeScript code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce slide source files, static HTML build guidance, and PDF export commands.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
