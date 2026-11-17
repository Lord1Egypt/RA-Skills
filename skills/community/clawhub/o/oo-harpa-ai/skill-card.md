## Description:

Operate HARPA AI through an OOMOL-connected account using the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to search and scrape web pages, run HARPA prompts, or execute HARPA AI commands through an existing OOMOL connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes downloaded software and may change skills used by other agents without explaining those changes.

Mitigation: Install and verify oo separately before running setup, review cross-agent skill changes, and use OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization when appropriate.

Risk: The remote installers and hosted connector implementation remain unverified.

Mitigation: Verify oo independently before allowing setup and keep approval requirements for destructive commands.

## Reference(s):

- [HARPA AI](https://harpa.ai/)
- [HARPA AI API reference](https://harpa.ai/grid/grid-rest-api-reference)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown instructions, shell command examples, and HARPA action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected HARPA AI action and connected browser session.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
