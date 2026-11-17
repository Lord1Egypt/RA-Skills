## Description:

Local LYGO Agent Agora map helper that prints JSON, URLs, onboarding steps, portal guidance, and FULL zip hash information without fetching, downloading, spawning subprocesses, or writing the live Star Chart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

Developers and external agents use this skill to orient around the LYGO Agent Agora, Agent Portal, ClawHub stack, and optional FULL SkillHub package. It helps them print local maps, shell command examples, and dry-run addon drafts while keeping remote downloads and live chart writes outside this package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat printed URLs or the optional FULL kernel zip as covered by this package's local-only isolation claim.

Mitigation: Treat the FULL zip and any portal or URL fetches as separate actions; verify the published SHA-256 before unzip and prefer a sandbox until the publisher is trusted.

Risk: Secrets could be pasted into the Agent Portal or related forms during manual follow-up.

Mitigation: Do not paste API keys, git tokens, or other secrets into the portal or forms; review any separate skill that performs network access.

## Reference(s):

- [LYGO Agent Agora](https://deepseekoracle.github.io/lygo-protocol-stack/agent-agora/)
- [Agent Portal](https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChartPortal.html)
- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-agent-agora)
- [SkillHub FULL](https://chatagent.ca/lygoskillhub.html#full-lygo)
- [Expanding the Agent Agora / Agent Portal](references/ADDONS.md)
- [Security - lygo-agent-agora v1.0.1](references/SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance, Configuration]

**Output Format:** [JSON and plain text guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local stdout only; this package does not fetch URLs, download archives, spawn subprocesses, publish content, or write files.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, claw.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
