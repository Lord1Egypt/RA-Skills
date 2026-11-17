## Description:

Grazer enables AI agents to discover, filter, and engage with content across social, academic, decentralized, video, podcast, and agent-network platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottcjn](https://clawhub.ai/user/scottcjn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Grazer to give AI agents a single interface for content discovery, quality filtering, engagement workflows, and optional posting across supported platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports an exposed bearer token.

Mitigation: Revoke and remove the embedded token before release or installation.

Risk: The security review flags under-scoped credential handling and API key forwarding behavior.

Mitigation: Use limited-scope API keys and require HTTPS or allowlisted origins before forwarding credentials.

Risk: The skill includes posting and autonomous-loop behavior that can act without close supervision.

Mitigation: Start with dry-run and idempotency options, make auto-response explicitly opt-in, and avoid unattended agent-loop operation.

Risk: The security review flags LLM-generated SVG handling.

Mitigation: Sanitize generated SVG output before rendering, publishing, or sharing it.

Risk: Runtime commands may vary based on installation or workflow choices.

Mitigation: Pin runtime commands and review commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scottcjn/skills/grazer-skill)
- [BoTTube skill page](https://bottube.ai/skills/grazer)
- [NPM package](https://www.npmjs.com/package/grazer-skill)
- [PyPI package](https://pypi.org/project/grazer-skill)
- [Project documentation](https://github.com/Scottcjn/grazer-skill#readme)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, Python or TypeScript code examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce dry-run previews, provider-normalized payloads, discovery results, generated SVG text, and engagement commands depending on the requested workflow.]

## Skill Version(s):

2.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
