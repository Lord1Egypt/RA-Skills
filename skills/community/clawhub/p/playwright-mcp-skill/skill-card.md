## Description:

Run browser automation through @playwright/mcp over UXC stdio MCP, with daemon-friendly session reuse and safe action guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to set up and run deterministic browser navigation, accessibility snapshots, clicks, and scripted page actions from CLI-driven agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable commands resolve @playwright/mcp@latest, so the executed package can change after review.

Mitigation: Prefer an exact pinned @playwright/mcp version or a locally installed reviewed binary before deployment.

Risk: Shared browser profiles may contain cookies or active login sessions.

Mitigation: Use isolated headless mode by default; when shared profiles are needed, use a dedicated low-privilege automation account and avoid concurrent profile use.

Risk: Browser automation can submit forms or trigger other high-impact page actions.

Mitigation: Start with navigation and snapshots, and require explicit confirmation before form submission, checkout, delete, or irreversible multi-step flows.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [ClawHub Skill Page](https://clawhub.ai/jolestar/skills/playwright-mcp-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON envelope parsing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes read-first browser inspection, fixed command linking, JSON envelope parsing, and confirmation before high-impact actions.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
