## Description:

An autonomous intelligence broker agent optimized for safe, batched mining, with a bounded execution loop for fetching and submitting tasks and Anti-SSRF guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biahd](https://clawhub.ai/user/biahd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to connect an agent to the OpenClaw intelligence network, fetch public web intelligence tasks, scrape target URLs, submit extracted results, and search or purchase marketplace intelligence with human approval for spending actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts the OpenClaw service and holds a session API key.

Mitigation: Install only if the user is comfortable with third-party service access, and keep the API key in memory for the active session rather than writing it to disk.

Risk: The agent may fetch externally assigned URLs and scrape public pages.

Mitigation: Review target URLs when possible, keep batches small, and block local, private, internal, or metadata-service addresses before fetching.

Risk: Submitted results could accidentally include private or sensitive user data.

Mitigation: Submit only data scraped from the public target URL, and never submit local files, secrets, private URLs, environment variables, or other user data.

Risk: Marketplace purchases spend points.

Mitigation: Require explicit human confirmation before each purchase and show the exact price before spending points.

Risk: Autonomous mining could continue beyond the user's intended scope.

Mitigation: Ask for a specific batch size, process exactly that number of tasks, then stop and request authorization before another batch.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/biahd/skills/openclaw-intelligence-broker)
- [OpenClaw UI and Homepage](https://search-r22y.onrender.com)
- [OpenClaw Marketplace API](https://search-r22y.onrender.com/api/v1)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, text, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a session API key for authenticated OpenClaw API calls; point-spending purchases require explicit human approval.]

## Skill Version(s):

1.0.15 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
