## Description:

LYGO Joy Loop Protocol helps agents run local Joy Loop ticks, snapshots, dashboards, and consent-gated planter commands in a LYGO protocol stack checkout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when they explicitly need to run or inspect Joy Loop behavior in a local LYGO protocol stack checkout. It supports local state ticks, snapshot reads, Architect dashboard commands, and consent-gated planting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running an unpinned or unverified copy could execute unexpected code in a local LYGO stack checkout.

Mitigation: Use a pinned ClawHub install or verify package provenance first, set LYGO_STACK_ROOT to a trusted absolute path, and confirm the expected LYGO stack scripts before execution.

Risk: Tier 1 Joy Loop ticks and live runtimes can update local state and a snapshot file that may become public if the repository is later pushed to GitHub Pages.

Mitigation: Warn the user before commands that update the snapshot when publishing may follow, and do not push or publish unless the user explicitly requests it.

Risk: Planting changes registry-related state and should not happen from ambiguous or implied consent.

Mitigation: Run planter flows only after explicit user consent, require --i-consent or LYGO_JOY_PLANT_CONSENT=yes, and avoid setting consent environment variables on the user's behalf.

Risk: Interactive dashboard or serve modes can expose local ports if configured incorrectly.

Mitigation: Use localhost defaults unless the user specifically requests another bind address, and avoid public tunnels or 0.0.0.0 bindings without explicit user direction.

## Reference(s):

- [LYGO Joy Loop Security and Disclosure](references/SECURITY.md)
- [Joy Loop Agent Contract](references/AGENT_CONTRACT.md)
- [LYGO Protocol Stack Repository](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [ClawHub Skill Listing](https://clawhub.ai/deepseekoracle/skills/lygo-joy-loop)
- [JoyLoopRegistry Public Mirror](https://deepseekoracle.github.io/lygo-protocol-stack/JoyLoopRegistry.json)
- [Joy Loop Snapshot Public Mirror](https://deepseekoracle.github.io/lygo-protocol-stack/joy_loop/joy_loop_snapshot.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [State-changing commands require confirmed stack location, tier disclosure, and user consent where applicable.]

## Skill Version(s):

2.3.1 (source: SKILL.md frontmatter metadata and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
