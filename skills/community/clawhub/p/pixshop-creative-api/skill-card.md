## Description:

Pixshop Developer REST API guides agents through Pixshop image generation and editing, video generation, prompts, apps, community endpoints, and HTTP integration examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizhijun](https://clawhub.ai/user/lizhijun)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to integrate Pixshop AI creative services into applications through REST endpoints, bearer-token authentication, curl examples, and JSON request and response patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer tokens may be exposed through chat transcripts, shell history, logs, or printed configuration files.

Mitigation: Treat Pixshop tokens as passwords, avoid echoing them in shared contexts, mask them in logs, and rotate them if exposure is suspected.

Risk: The skill suggests installing a global CLI before retrieving account credentials.

Mitigation: Prefer a pinned or isolated CLI install and review the package source and permissions before using it with account tokens.

Risk: Image tools may process face, person, clothing, or ID-photo media.

Mitigation: Upload images only with appropriate permission and after reviewing Pixshop service privacy and usage terms for sensitive media.

Risk: Pixshop API calls may consume credits, hit rate limits, or require polling for long-running video jobs.

Mitigation: Handle 402 and 429 responses, add retry or backoff logic, and poll asynchronous task IDs until completion or timeout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lizhijun/skills/pixshop-creative-api)
- [Pixshop](https://pixshop.app)
- [Nano Banana Apps](https://pixshop.app/apps)
- [Pixshop Prompt Library](https://pixshop.app/prompt-library)
- [Pixshop Design Agent](https://pixshop.app/agent)
- [Pixshop MCP endpoint](https://pixshop.app/api/mcp)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with endpoint tables, curl examples, and JSON request and response snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes bearer-token API usage, workflow notes, credit and rate-limit considerations, asynchronous task notes, and error-code guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
