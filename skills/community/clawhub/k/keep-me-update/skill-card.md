## Description:

Keep Me Update helps an agent produce daily tech, AI, and geek-news digests from RSS feeds plus web search after a first-run configuration flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nemocccc](https://clawhub.ai/user/nemocccc)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to configure an agent once, gather current technology news from RSS and web search, and receive a concise digest in the terminal or as a Markdown file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound HTTP requests to arbitrary RSS feed and news URLs.

Mitigation: Run it only in environments where this network access is acceptable, and avoid adding untrusted RSS feeds.

Risk: The README includes a curl-to-bash installer pattern for a related agent.

Mitigation: Inspect and pin any remote installer before executing it, or use a reviewed installation path.

Risk: The skill writes local configuration, cache, seen-guid state, and optional digest files.

Mitigation: Review the configured output directory and retention settings before enabling file output or cleanup.

## Reference(s):

- [Interactive Config Flow Pattern](references/config-flow.md)
- [RSS Feed Behavior Reference](references/feed-behavior.md)
- [Project homepage](https://github.com/Nemocccc/KeepMeUpdate)
- [ClawHub skill page](https://clawhub.ai/nemocccc/skills/keep-me-update)
- [Hermes Agent documentation](https://hermes-agent.nousresearch.com/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal text or Markdown digest with source links; helper scripts may emit JSON during collection.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write local user configuration, RSS cache, seen-guid state, and optional Markdown digest files.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
