## Description:

Nimble Real-Time Web Intelligence Tools guides an agent to use the Nimble CLI for live web search, content extraction, site mapping, and crawling with structured outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilchemla](https://clawhub.ai/user/ilchemla)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill when an agent needs current web research, URL extraction, site mapping, or larger website crawls through Nimble's external CLI service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web searches, target URLs, crawls, and extracted content may be handled by Nimble's external service.

Mitigation: Use only with data that is appropriate to share with the service, and avoid internal URLs, credentials, session cookies, or sensitive person-research queries without a clear lawful and privacy-appropriate basis.

Risk: The skill's setup guidance uses an unpinned global npm install for the Nimble CLI.

Mitigation: Prefer a pinned version or a locally controlled CLI installation before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ilchemla/skills/nimble-web-tools)
- [Publisher profile](https://clawhub.ai/user/ilchemla)
- [Source repository from metadata](https://github.com/Nimbleway/agent-skills)
- [Search focus modes reference](references/search-focus-modes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and Nimble CLI output options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route web searches, URL extraction, site mapping, and crawls through Nimble's external service; CLI output can be JSON, YAML, pretty-printed text, raw responses, markdown, plain text, or simplified HTML depending on command options.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
