## Description:

Autonomous browser automation for AI agents using agent-browser for step-by-step Playwright control and browser-use for autonomous page navigation, form filling, scraping, sessions, screenshots, and multi-step browser tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinj0012](https://clawhub.ai/user/yinj0012)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to automate dynamic browser workflows, including navigation, form entry, structured extraction, authenticated sessions, and autonomous multi-step research tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and autonomous browser wrapper introduce credential, privilege, and local code-execution risk.

Mitigation: Review before installing, run in an isolated unprivileged environment, avoid root execution unless audited, and pass narrowly scoped API keys explicitly.

Risk: Saved cookies, authentication state, screenshots, PDFs, or recordings can contain sensitive account data.

Mitigation: Avoid saving sensitive browser artifacts unless they can be protected, access-limited, and deleted after use.

Risk: Wrapper behavior can read provider keys from root OpenClaw configuration when environment keys are absent.

Mitigation: Do not rely on stored root provider keys; provide explicit, least-privilege keys for each task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinj0012/skills/openclaw-skill-browser-use)
- [Browser workflow reference](references/browser-workflow.md)
- [agent-browser npm package](https://www.npmjs.com/package/agent-browser)
- [browser-use Python library](https://github.com/browser-use/browser-use)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and Python code examples, plus command output from browser automation tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshots, PDFs, recordings, saved browser state, cookies, and extracted page content when the agent runs the referenced tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
