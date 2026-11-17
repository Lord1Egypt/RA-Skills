## Description:

Wrap a local openclaw_capture_workflow checkout as an OpenClaw/ClawHub skill that captures links, text, images, and videos, routes STT by platform, and fans results out to Telegram and Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[etherstrings](https://clawhub.ai/user/etherstrings)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send links, pasted text, images, and videos into a local OpenClaw capture workflow while preserving the legacy payload contract and selecting STT and notification routes by environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Capture payloads and summaries may be sent to configured HTTP backends, model APIs, Telegram, or Feishu.

Mitigation: Use trusted backend URLs, prefer HTTPS for remote services, scope API keys and bot tokens tightly, and dispatch private or proprietary content only when sharing with configured services is acceptable.

Risk: A configured local STT command can process media inputs and receive templated runtime arguments.

Mitigation: Enable only a reviewed, known-safe STT command and keep the default remote-only profile when a local command is not required.

Risk: The skill allows implicit invocation, which may dispatch sensitive text, image references, videos, or chat identifiers automatically.

Mitigation: Require review for sensitive capture requests and disable or constrain implicit invocation in environments that handle private or regulated content.

## Reference(s):

- [Runtime profiles and environment matrix](artifact/references/runtime-profiles.md)
- [Module behavior and output fanout](artifact/references/module-matrix.md)
- [Legacy payload contract and mixed-input rules](artifact/references/payload-contract.md)
- [ClawHub skill page](https://clawhub.ai/etherstrings/skills/openclaw-capture)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Acknowledgement text, JSON job status, Markdown notes, and notification messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes capture payloads through configured local or HTTP backends and optional Telegram or Feishu outputs.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
