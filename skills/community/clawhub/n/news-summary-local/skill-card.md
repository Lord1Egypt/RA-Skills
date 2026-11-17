## Description:

Local news summary skill that reads RSS/XML files in the workspace, extracts titles, and produces a concise list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fedrov2025](https://clawhub.ai/user/fedrov2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to inspect a local RSS/XML feed and return the first 10 item titles as a compact news summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running summarize.sh from an untrusted working directory can execute an attacker-controlled ./extract.sh helper.

Mitigation: Run the skill only from its trusted installation directory or update summarize.sh to resolve extract.sh relative to the script directory before use.

Risk: RSS/XML title extraction uses simple grep/sed matching, so malformed feeds or uncommon XML formatting may produce incomplete or misleading summaries.

Mitigation: Review the output against the source feed for important use cases and prefer a structured XML parser if higher accuracy is required.

## Reference(s):

- [News Summary Local on ClawHub](https://clawhub.ai/fedrov2025/skills/news-summary-local)
- [fedrov2025 Publisher Profile](https://clawhub.ai/user/fedrov2025)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text title list with shell command usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to news.rss when no RSS file path is provided and prints up to 10 extracted title values.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
