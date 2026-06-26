## Description: <br>
MagicBrowse provides a browser automation fallback through the magicbrowse CLI, using goal-driven act by default and observation or primitives only for recovery with fresh page-state verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xor777](https://clawhub.ai/user/xor777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use MagicBrowse when their native page-control tool cannot reliably navigate a web flow. It helps reach pages, inspect state, and prepare non-sensitive browser tasks while stopping at credentials, payment, identity, CAPTCHA, or consequential actions unless the workflow has explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LLM-backed browser automation sends page context, and vision mode can send screenshots, to the MagicBrowse gateway. <br>
Mitigation: Use fresh browser sessions for normal tasks, avoid private pages unless the workflow is approved, and use vision mode only when the user accepts sharing screenshots for that task. <br>
Risk: The workflow may reach login, identity, payment, CAPTCHA, or other sensitive boundaries. <br>
Mitigation: Stop at those boundaries, surface the handoff to the user or approved orchestrator, and do not invent or enter credentials, identity data, payment data, CAPTCHA answers, or memory-managed values. <br>
Risk: Attaching to an existing CDP endpoint, browser profile, or user data directory inherits the authority of that browser session. <br>
Mitigation: Use an owned fresh browser by default, attach only after explicit approval for the current task, keep CDP endpoints private, and avoid closing user-owned sessions without teardown approval. <br>
Risk: Browser primitives can execute a click or input without proving that the intended page state changed. <br>
Mitigation: Prefer act for goal-directed steps and re-run observe after primitive actions before making the next decision. <br>
Risk: The next browser action may commit an account-affecting or irreversible change. <br>
Mitigation: Ask for explicit approval for the exact visible action, re-observe after approval, and execute only the approved final action while page facts remain unchanged. <br>


## Reference(s): <br>
- [MagicBrowse CLI package](https://www.npmjs.com/package/@mercuryo-ai/magicbrowse-cli) <br>
- [OpenClaw marketplace README](https://github.com/MercuryoAI/skills/blob/main/docs/magicbrowse/openclaw/marketplace/README.md) <br>
- [MagicBrowse Command Guide](https://github.com/MercuryoAI/skills/blob/main/docs/magicbrowse/references/commands.md) <br>
- [MagicBrowse Guardrails](https://github.com/MercuryoAI/skills/blob/main/docs/magicbrowse/references/guardrails.md) <br>
- [MagicBrowse Statuses](https://github.com/MercuryoAI/skills/blob/main/docs/magicbrowse/references/statuses.md) <br>
- [MagicBrowse Worked Example](https://github.com/MercuryoAI/skills/blob/main/docs/magicbrowse/references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, json] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the magicbrowse CLI and MAGICPAY_API_KEY; act results may include status, finalUrl, finalMessage, blockedReason, and handoff metadata.] <br>

## Skill Version(s): <br>
0.1.16 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
