## Description:

LYRA OpenClaw Hybrid is a public map for installing and operating a consent-gated LYRA + OpenClaw stack with browser, Discord, social, token-launch, memory, and local-model workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

LYGO Sovereign License v2.0

## Use Case:

External operators and developers use this skill to understand the public LYRA + OpenClaw architecture, install related ClawHub skills, and apply consent and secret-handling rules before using external automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned related skill installs and external stack components may introduce behavior outside this package.

Mitigation: Review and pin the ClawHub installer, each related skill, and the external OpenClaw/LYRA stack before installing or granting elevated access.

Risk: Browser-write, Discord, social posting, token-launch, memory, and local-secret workflows can affect live systems or expose sensitive material.

Mitigation: Use an isolated environment without production secrets or wallet material until the full stack is verified, and require explicit human approval before external actions.

Risk: Secrets could be pasted into chat logs or stored in memory layers during operation.

Mitigation: Load credentials only from operator-controlled local stores at runtime and keep secrets out of prompts, logs, public feeds, and memory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lyra-open-claw)
- [LYGO Protocol Stack](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [Security Notes](references/SECURITY.md)
- [SkillSpector Audit](references/SKILLSPECTOR_AUDIT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs the agent toward consent-gated operation and local secret handling; no runtime credentials are included.]

## Skill Version(s):

1.0.0 (source: frontmatter, claw.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
