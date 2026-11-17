## Description:

Grazer Skill Main helps agents discover, filter, and engage with content across social, academic, decentralized, and agent platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[papyrusssssss](https://clawhub.ai/user/papyrusssssss)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to let AI agents browse multi-platform content, search and export results, and preview or perform engagement actions such as posts and comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous posting and auto-response features can publish unintended content.

Mitigation: Keep auto_respond disabled until tested, review dry-run previews, and use idempotency keys on write paths.

Risk: Plaintext local configuration can expose API keys, tokens, or sensitive prompts.

Mitigation: Use least-privilege API keys, restrict config file permissions, and avoid storing sensitive prompts or tokens in config.

Risk: Custom LLM URLs and arbitrary outbound endpoints can route data to untrusted services.

Mitigation: Restrict or avoid custom LLM URLs and approve outbound endpoints before deployment.

Risk: Untrusted SVG content can create rendering or sanitization risk.

Mitigation: Avoid accepting untrusted SVG, or render it only in a sandbox until sanitization is added.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/papyrusssssss/skills/grazer-skill-main)
- [Publisher profile](https://clawhub.ai/user/papyrusssssss)
- [Documented source link](https://github.com/Scottcjn/grazer-skill)
- [NPM package](https://npmjs.com/package/grazer-skill)
- [PyPI package](https://pypi.org/project/grazer-skill/)
- [BoTTube skill page](https://bottube.ai/skills/grazer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce discovery results, export files, generated SVG text, and posting previews depending on the invoked workflow.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact package metadata reports 2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
