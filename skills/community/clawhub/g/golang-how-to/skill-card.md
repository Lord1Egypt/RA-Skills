## Description:

Golang How To routes Go coding, review, debugging, setup, package lookup, and configuration tasks to the most relevant Go skills from samber/cc-skills-golang.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers working on Go projects use this skill to select the right Go guidance for coding, review, debugging, project setup, package lookup, and code navigation. In configure mode, it can also help set project agent configuration so Go work loads the intended skills consistently.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct agents to modify persistent project agent configuration files, which may cause future sessions to auto-load Go skills without the user's intent.

Mitigation: Review exact diffs before allowing changes to CLAUDE.md, AGENTS.md, GEMINI.md, Cursor rules, or Copilot instructions, and only keep them when that future behavior is wanted.

Risk: The install metadata uses gopls@latest, which can change over time.

Mitigation: Pin a known gopls version for reproducible setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-how-to)
- [Publisher profile: samber](https://clawhub.ai/user/samber)
- [Project homepage](https://github.com/samber/cc-skills-golang)
- [Golang skills catalog by category](artifact/references/by-category.md)
- [Competing clusters disambiguation](artifact/references/disambiguation.md)
- [Configure mode project config](artifact/references/project-config.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code, shell command, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires go, git, and gopls for full Go navigation and refactoring support.]

## Skill Version(s):

1.4.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
