## Description:

Guides agents through choosing web_search, web_fetch, opencli, or browser workflows, including fallback behavior, login handling, and search API configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freeman88-tch](https://clawhub.ai/user/freeman88-tch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to plan web information retrieval, select the appropriate web tool, handle failures, and request user confirmation before login or sensitive browser actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can install a global npm package and download a browser extension from a GitHub release.

Mitigation: Review and trust the opencli package and extension source before running the setup script, preferably in a non-sensitive environment.

Risk: The configuration flow may involve API keys and persistent local configuration changes.

Mitigation: Use secure local secret handling for API keys and avoid pasting credentials into chat.

Risk: The setup script can restart browser or gateway processes and make persistent local changes.

Mitigation: Run it only on machines where browser restart, gateway restart, and local configuration changes are acceptable.

Risk: Browser or opencli workflows may involve login or sensitive write actions.

Mitigation: Require explicit user confirmation before login, posting, deleting, payment, or other state-changing actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/freeman88-tch/skills/lobster-web-tools)
- [OpenCLI Guide](artifact/references/opencli-guide.md)
- [Web Search API Configuration](artifact/references/web-search-config.md)
- [Well-Known Sites Index](artifact/references/well-known-sites.json)
- [OpenCLI GitHub Releases](https://github.com/jackwener/opencli/releases)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with inline shell commands and structured configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to read local reference files before continuing web-search configuration or fallback workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
