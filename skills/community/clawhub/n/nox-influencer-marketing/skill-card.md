## Description: <br>
Runs NoxInfluencer creator discovery and marketing-ops workflows for influencer sourcing, creator evaluation, outreach operations, campaign and collection management, CRM/email/product-center workflows, brand monitoring, and exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noxinfluencer](https://clawhub.ai/user/noxinfluencer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams and agents use this skill to discover and evaluate creators across YouTube, TikTok, and Instagram, operate NoxInfluencer campaign and outreach workflows, retrieve approved contact exports, monitor videos, and summarize brand-monitor data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill lets an agent operate a NoxInfluencer account and may prepare sensitive sends, schedules, CRM changes, contact exports, unlocks, or downloads. <br>
Mitigation: Install only when this account access is intended, review actions before approval, and require explicit approval gates before sensitive writes or exports. <br>
Risk: NoxInfluencer login stores a reusable local API key. <br>
Mitigation: Use normal local credential hygiene for the CLI environment and remove or rotate access if the workspace is shared or no longer trusted. <br>


## Reference(s): <br>
- [NoxInfluencer Skill Homepage](https://www.noxinfluencer.com/skills) <br>
- [ClawHub Release Page](https://clawhub.ai/noxinfluencer/nox-influencer-marketing) <br>
- [Brand Monitor Workflows](references/brand-monitor.md) <br>
- [CLI Response Format](references/cli-response-format.md) <br>
- [Marketing Ops Workflows](references/marketing-ops.md) <br>
- [Platform Support](references/platform-support.md) <br>
- [Search Filter Semantics](references/search-filters.md) <br>
- [Verdict Heuristics Reference](references/verdict-heuristics.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Concise plain-language summaries with structured Markdown and agent-executed CLI operations when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May preserve creator IDs, task IDs, export IDs, pagination state, quota blockers, and approval status for follow-up workflows.] <br>

## Skill Version(s): <br>
0.1.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
