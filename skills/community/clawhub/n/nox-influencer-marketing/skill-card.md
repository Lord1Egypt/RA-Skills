## Description:

Operate NoxInfluencer creator intelligence and marketing systems through the CLI, including search, analysis, contacts, monitoring, campaigns, CRM, outreach operations, products, affiliation, brand intelligence, exports, account setup, quota, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noxinfluencer](https://clawhub.ai/user/noxinfluencer)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers and business teams use this skill to discover creators, assess fit and risk, manage NoxInfluencer campaign operations, run approved outreach workflows, export records, and troubleshoot account, quota, or CLI issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned third-party CLI package.

Mitigation: Review the NoxInfluencer CLI package before installation and prefer a pinned, trusted version.

Risk: Authenticated CLI actions can affect outreach, CRM, exports, account state, product records, and paid or quota-consuming operations.

Mitigation: Use a restricted NoxInfluencer account, keep credentials scoped and revocable, and require explicit confirmation before sends, schedules, exports, unlocks, CRM changes, product changes, or deletions.

## Reference(s):

- [NoxInfluencer Skill Page](https://www.noxinfluencer.com/skills)
- [ClawHub Skill Release](https://clawhub.ai/noxinfluencer/skills/nox-influencer-marketing)
- [NoxInfluencer Usage Billing](https://www.noxinfluencer.com/skills/usage-billing)
- [CLI Response Format](references/cli-response-format.md)
- [Marketing Ops Workflows](references/marketing-ops.md)
- [Brand Monitor Workflows](references/brand-monitor.md)
- [Platform Support](references/platform-support.md)
- [Search Filter Semantics](references/search-filters.md)
- [Verdict Heuristics Reference](references/verdict-heuristics.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain-language Markdown summaries with verified IDs, system state, and action URLs when user action is required.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or download files through approved NoxInfluencer CLI workflows; write actions require explicit approval and dry-run or preview where supported.]

## Skill Version(s):

0.1.18 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
