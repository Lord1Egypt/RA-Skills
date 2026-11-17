## Description:

God's eye view of your dev repos. Multi-project tracking across GitHub/Azure DevOps. AI learns from your commits to upgrade your agents.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wetzja04-dot](https://clawhub.ai/user/wetzja04-dot)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use this skill to track activity across development repositories, summarize commits, pull requests, and issues, and produce recommendations for improving agent instruction files from observed commit patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository instruction content, commit summaries, and metadata may be exposed to the active agent or configured LLM providers during analysis.

Mitigation: Run analysis only on repositories whose contents are appropriate for the selected agent or LLM provider, and review provider configuration before analyzing private repositories.

Risk: The skill can propose or apply changes to AGENTS.md using existing repository access.

Mitigation: Review generated diffs before allowing commits, pushes, or GitHub API updates.

Risk: The release documents a remote installer pattern.

Mitigation: Review the installer first or install from a pinned release rather than piping a remote script directly into a shell.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wetzja04-dot/skills/god-mode-skill)
- [Publisher profile](https://clawhub.ai/user/wetzja04-dot)
- [GitHub CLI documentation](https://cli.github.com/)
- [Configuration example](config.example.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Conversational Markdown with inline shell commands, summaries, and optional JSON command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to AGENTS.md or related agent instruction files for user review.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
