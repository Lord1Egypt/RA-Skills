## Description:

HMR Memory connects an agent to a local HMR service to save preferences and facts, recall relevant context, and restore task state across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snowfoxhq](https://clawhub.ai/user/snowfoxhq)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to add durable local memory to OpenClaw agents, including saving user preferences, recalling relevant past context, and resuming paused work across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-term memory can retain sensitive or untrusted content and influence future agent behavior.

Mitigation: Store only information the user directly shared and is safe to retain; avoid secrets, passwords, API keys, scraped web pages, and third-party messages.

Risk: Exposing the HMR service beyond localhost can increase access and privacy risk.

Mitigation: Keep the service bound to localhost and do not expose it outside the local machine.

Risk: The skill depends on a separately obtained local HMR service and its runtime dependencies.

Mitigation: Obtain the HMR service from a trusted source and use a virtual environment or container with pinned dependencies where possible.

## Reference(s):

- [HMR project homepage](https://github.com/snowfoxHQ/HMR)
- [ClawHub skill page](https://clawhub.ai/snowfoxhq/skills/hmr-memory)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance, Configuration instructions]

**Output Format:** [Markdown guidance with JSON HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local HMR service on http://127.0.0.1:8077; an optional HMR_TOKEN header may be used when configured.]

## Skill Version(s):

1.1.0 (source: frontmatter, package.json, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
