## Description:

Private Search guides OpenClaw agents to configure Brave Search, Kagi, or SearXNG as privacy-oriented search providers and strip tracking parameters from result URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[u4ma-kev](https://clawhub.ai/user/u4ma-kev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure privacy-oriented web search providers for agent research workflows, with Brave Search as the default and optional Kagi or self-hosted SearXNG settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes strong privacy and search-override claims that the package evidence does not prove.

Mitigation: Verify in OpenClaw that the claimed search routing is implemented and tested before relying on the privacy guarantee.

Risk: The setup script can display part of the Brave API key, save the key in plaintext, and send it to Brave during the test request.

Mitigation: Use a limited-purpose API key, avoid storing it in a shared $HOME/.env file, check file permissions, and rotate the key if it may have been exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/u4ma-kev/skills/private-search)
- [Privacy Search Engines Reference Guide](references/privacy-engines.md)
- [Brave Search API Documentation](https://api.search.brave.com/app/documentation/)
- [Kagi API Documentation](https://help.kagi.com/kagi/api/)
- [SearXNG Documentation](https://docs.searxng.org/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration variables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BRAVE_API_KEY for the default Brave Search setup; KAGI_API_KEY and SEARXNG_URL are optional provider-specific settings.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
