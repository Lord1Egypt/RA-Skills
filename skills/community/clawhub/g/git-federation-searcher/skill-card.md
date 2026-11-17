## Description:

Search across multiple self-hosted Git instances including Gitea, Forgejo, GitLab, and Codeberg. Aggregates search results from Codeberg.org, Gitea.com, OpenDev, NotABug, and Gitdab. Supports API-based search with fallback to web search via SearXNG. Allows adding custom private instances with API token support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djswiss](https://clawhub.ai/user/djswiss)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to search public or configured self-hosted Git forges from a command line or Telegram command interface, aggregate matching repositories, and sort results by popularity signals such as stars.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports exploitable command execution risk in the web-search fallback.

Mitigation: Remove the shell=True fallback or replace it with constrained argument-based execution before installing in shared, bot-accessible, or privileged environments.

Risk: The release evidence reports under-scoped handling for custom instance URLs.

Mitigation: Restrict custom instance URLs to approved hosts or network ranges before allowing untrusted users to add instances.

Risk: The release evidence reports credential handling concerns for API tokens.

Mitigation: Move API tokens out of plaintext configuration and URL parameters before using the skill with private instances.

Risk: The release evidence flags Telegram command usage as unsafe without administrative controls.

Mitigation: Add Telegram administrative checks before exposing add, remove, enable, or disable commands through a bot.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/djswiss/skills/git-federation-searcher)
- [Codeberg](https://codeberg.org)
- [Gitea.com](https://gitea.com)
- [OpenDev](https://opendev.org)
- [NotABug](https://notabug.org)
- [Gitdab](https://gitdab.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text search results with repository names, URLs, descriptions, stars, forks, language, and instance metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can list, add, remove, enable, or disable configured Git instances; searches are aggregated across enabled instances.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
