## Description:

Use when publishing a SKILL.md-style agent skill across uGig, sh1pt, GitHub/gists, and follow-on skill marketplaces such as ClawHub, Goose, LobeHub, Kilo, Skillstore, FreeMyGent, ClawMart, Manus, VS Code Agent Skills, and Moltbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ralyodio](https://clawhub.ai/user/ralyodio)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill maintainers use this skill to package, publish, and promote SKILL.md-style agent skills across ClawHub, uGig, sh1pt, GitHub or gists, and related marketplaces. It helps prepare public-safe metadata, publishing commands, marketplace checklists, and final status reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended pre-publish secret scan can inspect and print sensitive data from the whole working directory.

Mitigation: Run the scan only against the target SKILL.md or in a clean staging directory, then review every public upload command before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ralyodio/skills/promote-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/ralyodio)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, marketplace checklists, configuration guidance, and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include marketplace URLs, dry-run publishing commands, public source recommendations, and security review notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
