## Description:

maimai-cli helps agents use the local Maimai CLI to import login state, inspect feeds and hot rankings, search content, read post details and comments, download images, and troubleshoot login issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariotong](https://clawhub.ai/user/mariotong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to route Maimai-related requests to the local maimai CLI, including account status checks, feed and hot-rank reading, search, post details, comments, image handling, profile lookup, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Maimai Cookie or session values could be exposed if pasted into chat or echoed from local storage.

Mitigation: Import Cookies from the user's own terminal, avoid repeating sensitive values, and use maimai logout or a fresh login if a Cookie may have been exposed.

Risk: The skill depends on an external maimai-cli installation.

Mitigation: Install only a trusted or pinned maimai-cli release before using the skill.

Risk: Image downloads can write files to local directories chosen during use.

Mitigation: Choose download directories deliberately and review paths before running image download commands.

## Reference(s):

- [maimai-cli project homepage](https://github.com/mariotong/maimai-cli)
- [Authentication and safety](references/auth.md)
- [Feed reading](references/feeds.md)
- [Search and discovery](references/search.md)
- [Details, comments, images, and profiles](references/detail.md)
- [Troubleshooting and workflows](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON or YAML CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local maimai command; may guide users to download images or request structured CLI output when appropriate.]

## Skill Version(s):

1.1.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
