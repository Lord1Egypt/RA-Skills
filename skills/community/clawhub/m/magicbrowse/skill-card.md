## Description:

Browser automation fallback through the magicbrowse CLI with goal-driven act as the default primitive and observe/primitives only for recovery, with changed page state verified by fresh observation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xor777](https://clawhub.ai/user/xor777)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use MagicBrowse when their runtime's native page-control tool cannot reliably navigate public web workflows. It helps reach target pages, inspect page state, prepare non-sensitive actions, and stop at approval, authentication, CAPTCHA, payment, identity, or memory-fill boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release installs a mutable third-party CLI package.

Mitigation: Trust the publisher and gateway before installation; prefer pinning an exact CLI version and installing locally or in a sandbox.

Risk: Browser page context and vision-mode screenshots can leave the browser through the LLM-backed gateway.

Mitigation: Avoid private or sensitive pages unless the user has approved the workflow, and use vision mode only when the user is comfortable sending screenshots or page context.

Risk: Gateway-provided failure messages may influence agent behavior.

Mitigation: Treat gateway messages as status text, branch on structured status fields, and use documented approval stops for consequential actions.

Risk: Shared MagicBrowse session state can create cross-talk between parallel workflows.

Mitigation: Use a distinct MAGICBROWSE_HOME per workflow or avoid running multiple MagicBrowse tasks against the same home concurrently.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xor777/skills/magicbrowse)
- [OpenClaw Marketplace README](https://github.com/nuanu-ai/skills/blob/main/docs/magicbrowse/openclaw/marketplace/README.md)
- [MagicBrowse CLI Package](https://www.npmjs.com/package/@nuanu-ai/magicbrowse-cli)
- [MagicBrowse Command Guide](https://github.com/nuanu-ai/skills/blob/main/docs/magicbrowse/references/commands.md)
- [MagicBrowse Workflow Example](https://github.com/nuanu-ai/skills/blob/main/docs/magicbrowse/references/workflow.md)
- [MagicBrowse Guardrails](https://github.com/nuanu-ai/skills/blob/main/docs/magicbrowse/references/guardrails.md)
- [MagicBrowse Statuses](https://github.com/nuanu-ai/skills/blob/main/docs/magicbrowse/references/statuses.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON, Text]

**Output Format:** [Markdown guidance with inline shell commands and CLI JSON/text results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MAGICPAY_API_KEY for gateway setup and the magicbrowse CLI for browser sessions.]

## Skill Version(s):

0.1.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
