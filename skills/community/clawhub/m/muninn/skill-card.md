## Description:

Muninn provides a local MCP memory and CXP indexing layer for AI agents to initialize projects, search project context, and store project memories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[endgegnerbert-tech](https://clawhub.ai/user/endgegnerbert-tech)

### License/Terms of Use:

UNLICENSED

## Use Case:

Developers and AI-agent operators use Muninn to give agents project-local memory, semantic context search, and persistent notes for codebase work. It is intended for local workspaces where indexing and memory files can be reviewed by the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently write agent instructions into files that other AI agents may obey.

Mitigation: Install and test it only in a contained workspace, then review changes to CLAUDE.md, .cursorrules, and .antigravityrules before allowing agents to rely on them.

Risk: The skill watches and indexes project directories and stores local memories and indexes.

Mitigation: Use it only on intended projects, avoid sensitive workspaces unless local indexing is acceptable, and inspect or delete .muninn contents when needed.

Risk: Security evidence reports insufficient path scoping for project selection and memory writes.

Mitigation: Provide explicit project paths, run from a contained working directory, and verify that generated memories and indexes stay inside the intended project.

## Reference(s):

- [Muninn homepage](https://www.muninn.space)
- [ClawHub skill page](https://clawhub.ai/endgegnerbert-tech/skills/muninn)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [MCP text responses with local Markdown memory and context files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update .muninn project state, Markdown memory files, .gitignore entries, and agent rule files in the selected workspace.]

## Skill Version(s):

2.3.7 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
