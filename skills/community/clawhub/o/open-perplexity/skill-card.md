## Description:

Opens Brave browser to Perplexity AI. Access the AI-powered search engine that combines chat with real-time web search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to open Perplexity AI in Brave for citation-oriented AI search, real-time web lookup, and research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may activate the browser launcher when the user intended a more general web-search request.

Mitigation: Review and narrow trigger phrases before deployment in shared or production agent environments.

Risk: The Windows launch path uses shell=True for the Brave start command.

Mitigation: Review process-launch behavior on Windows and prefer an argument-list invocation where the runtime supports it.

Risk: The skill depends on Brave being installed and reachable on the host system path.

Mitigation: Confirm Brave installation and command availability on target Windows, macOS, and Linux hosts before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruchir17-cmd/skills/open-perplexity)
- [Perplexity AI](https://www.perplexity.ai/)
- [Brave Browser](https://brave.com)

## Skill Output:

**Output Type(s):** [Shell commands, Text]

**Output Format:** [Browser launch action with a short text confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Brave browser and an internet connection; no API key or credential storage is indicated.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
