## Description:

Generates or upgrades persistent repository instructions that encode Kinema's TDD methodology for Python and TypeScript/JavaScript projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeshunee](https://clawhub.ai/user/leeshunee)

### License/Terms of Use:

GNU General Public License v3.0

## Use Case:

Developers and engineering teams use this skill to initialize or upgrade repository-level TDD guidance before implementation work. It produces tailored agent instruction files for supported Python and TypeScript/JavaScript repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes persistent repository agent instructions that can influence future agent behavior.

Mitigation: Confirm the exact target file and review the generated diff before accepting changes.

Risk: The skill can write application configuration code when a custom configuration source is requested.

Mitigation: Avoid the custom config.py path unless you explicitly want application code changed.

Risk: The renderer depends on Jinja2 at execution time.

Mitigation: Use a pinned or locked Jinja2 environment when running the renderer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leeshunee/skills/kinema-tdd-injector)
- [README](artifact/README.md)
- [Kinema TDD Injector Onboarding](artifact/references/ONBOARDING.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instruction file content with supporting shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent repository agent instructions after target detection, questionnaire input, rendering, and diff review.]

## Skill Version(s):

1.4.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
