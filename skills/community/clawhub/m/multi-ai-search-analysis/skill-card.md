## Description:

Coordinates multiple AI assistants to analyze the same complex topic independently and synthesize a comparative Markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangsaizz](https://clawhub.ai/user/zhangsaizz)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, developers, and business users use this skill to ask the same complex question across several AI platforms and compare the resulting perspectives, data points, and recommendations. It is suited to market research, technical comparisons, product evaluations, trend analysis, and other work where cross-checking multiple model responses is useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analysis topics and prompts are submitted to third-party AI providers through logged-in user accounts.

Mitigation: Do not submit secrets, regulated data, or confidential business information; use only topics that are appropriate for the selected providers' terms and data handling.

Risk: The skill uses a persistent browser profile to retain login state for multiple AI services.

Mitigation: Use a dedicated browser profile or separate OS account, periodically remove stored browser state, and avoid sharing the profile directory.

Risk: Installer and browser automation choices include unsafe practices such as shell-based install commands, unpinned dependencies, and --no-sandbox browser flags.

Mitigation: Review scripts before execution, pin dependency versions, replace shell-based installer steps where possible, and remove --no-sandbox unless it is explicitly required in the deployment environment.

Risk: Generated comparative reports may contain inaccurate or unsupported claims from upstream AI systems.

Mitigation: Review the final report and verify important facts against authoritative sources before sharing, publishing, or using it for decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhangsaizz/skills/multi-ai-search-analysis)
- [artifact/SKILL.md](artifact/SKILL.md)
- [artifact/README.md](artifact/README.md)
- [artifact/scripts/USAGE.md](artifact/scripts/USAGE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, command-line status text, and local report/chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports are written under reports/ with timestamps; optional chart generation may write chart files under reports/charts/.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
