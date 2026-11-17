## Description:

Use when AI agents need to read, inspect, operate, navigate, debug, or verify browser state through the omnibot CLI and connected Chromium extension.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisjcy](https://clawhub.ai/user/dennisjcy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect AI agents to a live Chromium browser for logged-in, client-rendered workflows. It guides agents through reading pages, inspecting UI state, clicking controls, filling forms, navigating, collecting evidence, and verifying results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates in live logged-in browser sessions and may expose authenticated page content, cookies, screenshots, clipboard data, or network logs.

Mitigation: Use a dedicated browser profile and test accounts where possible, and treat captured browser evidence as sensitive.

Risk: Browser automation can submit, purchase, delete, publish, or otherwise change account data.

Mitigation: Require explicit human approval before irreversible or account-changing actions.

Risk: The workflow depends on a mutable globally installed Omnibot CLI package.

Mitigation: Pin and verify the CLI package before installation or deployment.

Risk: The artifact documents automated captcha-solving workflows.

Mitigation: Review intended use against site terms and require human oversight for captcha-related flows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dennisjcy/skills/omnibot-skills)
- [Chrome Web Store extension page](https://chromewebstore.google.com/detail/fojlpefamkmjbboafmjkkaejohagbdgn)
- [SkillHub listing](https://skillhub.cn/skills/omnibot)
- [Omnibot Command Reference](artifact/references/command-reference.md)
- [Operation Patterns](artifact/references/operation-patterns.md)
- [Workflow Context and Tabs](artifact/references/session-and-tabs.md)
- [Debugging and Evidence](artifact/references/debugging-and-evidence.md)
- [Runtime and Status](artifact/references/runtime-and-status.md)
- [Fallback Operations](artifact/references/fallback-operations.md)
- [Anti-Patterns](artifact/references/anti-patterns.md)
- [CSS-Only Dropdown JavaScript Recipe](artifact/references/css-only-dropdown-js.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Omnibot CLI, local daemon, and connected Chromium extension.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
