## Description:

Turns a page-story markdown file into a polished single-file static HTML page through design context gathering, design system generation, implementation planning, build, and quality review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xy-showing](https://clawhub.ai/user/xy-showing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and content owners use this skill to convert structured profile or project markdown into a static HTML page with traceable design choices and quality checks. It is especially aimed at personal, academic, portfolio, and professional profile pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is a bundle of multiple helper skills, so installed behavior may be broader than a single page builder.

Mitigation: Review the full bundled skill set before installation and enable only the skills needed for the intended workflow.

Risk: An included persistence script can write outside its intended folder.

Mitigation: Avoid using --persist with untrusted project or page names and review generated paths before running commands.

Risk: Setup guidance uses mutable package installs.

Mitigation: Pin package versions and install dependencies before placing API keys or other secrets in the environment.

Risk: Generated Markdown and HTML may be reused as agent context or published output.

Mitigation: Inspect generated files for accuracy, content fidelity, and unwanted instructions before relying on or publishing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xy-showing/skills/pageclaw)
- [Project homepage](https://github.com/XY-Showing/pageclaw)
- [page-claw README](artifact/skills/page-claw/README.md)
- [page-story starter](artifact/skills/page-claw/page-story-starter.md)
- [Simple Icons](https://simpleicons.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, generated Markdown planning files, and single-file static HTML code.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create page-story.md when no source brief exists, writes docs/plans/YYYY-MM-DD-<name>-design.md and docs/plans/YYYY-MM-DD-<name>-impl.md, and produces index.html for browser viewing.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
