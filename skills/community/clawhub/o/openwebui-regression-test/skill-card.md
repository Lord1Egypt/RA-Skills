## Description:

Regression-test Open WebUI tools, adapters, streaming, reconnects, provider limits, and TTS through the real browser path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinguy](https://clawhub.ai/user/pinguy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to verify Open WebUI regressions through the logged-in browser path, map failures to the responsible layer, apply narrow fixes, and report tested boundaries honestly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect logs, stored chat records, browser-visible behavior, and a logged-in Open WebUI app session during live-environment regression testing.

Mitigation: Use it only where the operator is authorized to test the environment, preserve existing database and user state, and remove only disposable test chats.

Risk: Regression testing can create provider rate pressure when repeated requests exercise adapters, streaming, tools, and TTS.

Mitigation: Use bounded retries only when safe, follow provider-directed or exponential backoff, disable avoidable incidental model calls, and avoid deliberately hammering providers.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/pinguy/Skills/tree/main/skills/openwebui-regression-test)
- [ClawHub skill page](https://clawhub.ai/pinguy/skills/openwebui-regression-test)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with diagnostic findings, narrow remediation steps, validation receipts, and tested boundaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
