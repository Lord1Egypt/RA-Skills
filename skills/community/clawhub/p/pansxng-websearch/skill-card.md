## Description:

Pansxng Websearch provides a local SearXNG-based meta-search workflow for multi-engine web search, private local search, engine selection, and category-based queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to run web searches through a local SearXNG instance, aggregate results from multiple engines, and request formatted search results or raw JSON from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ordinary search requests may change the host system by installing Homebrew, Python, Valkey, and SearXNG, modifying shell configuration, pulling unpinned network code, and leaving local services running.

Mitigation: Install only after reviewing and approving setup behavior; prefer a release that separates setup from search, asks for explicit confirmation, pins and verifies dependencies, uses a private app directory, and documents uninstall steps.

Risk: The security verdict is suspicious because setup and service lifecycle actions can happen automatically during normal use.

Mitigation: Run in a disposable or controlled environment first, inspect generated configuration, and stop local services after testing if they are not needed.

## Reference(s):

- [Pansxng Websearch on ClawHub](https://clawhub.ai/dashiming/skills/pansxng-websearch)
- [SearXNG upstream repository](https://github.com/searxng/searxng.git)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Formatted text search results or raw JSON, with command-line status and setup messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return fallback error JSON when local SearXNG is unavailable.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
