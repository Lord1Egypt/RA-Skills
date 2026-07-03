## Description: <br>
Runs NoxInfluencer creator and marketing-ops workflows via CLI, including creator discovery for influencer marketing, creator marketing, UGC, social media marketing, and affiliate marketing; creator evaluation, contact retrieval for external use, video tracking, campaigns, collections, CRM channels, product center, short links, email/message tasks, brand monitoring, and exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noxinfluencer](https://clawhub.ai/user/noxinfluencer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, creator partnerships operators, and agents use this skill to discover and evaluate creators, manage NoxInfluencer outreach workflows, monitor campaigns, retrieve approved contact data, and operate campaign, collection, CRM, product, short-link, export, and brand-monitor tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a NoxInfluencer account through the official CLI, including changes to campaigns, CRM records, email/message tasks, products, short links, and brand-monitor records. <br>
Mitigation: Use dry-run, validate, or preview paths where available and execute writes only after the user approves the exact object and action. <br>
Risk: The skill may retrieve visible creator contact information or create exports when explicitly requested. <br>
Mitigation: Limit contact retrieval and exports to explicit user requests, report only the needed visible contact details, and preserve export IDs and output paths for auditability. <br>
Risk: The CLI may rely on a locally stored API key and account quota or entitlements. <br>
Mitigation: Use browser login or stdin-based key handling, run diagnostics and quota checks before blocked workflows, and pass through service-provided action links for billing or authorization issues. <br>


## Reference(s): <br>
- [NoxInfluencer Skills Homepage](https://www.noxinfluencer.com/skills) <br>
- [CLI Response Format](references/cli-response-format.md) <br>
- [Marketing Ops Workflows](references/marketing-ops.md) <br>
- [Brand Monitor Workflows](references/brand-monitor.md) <br>
- [Platform Support](references/platform-support.md) <br>
- [Search Filter Semantics](references/search-filters.md) <br>
- [Verdict Heuristics Reference](references/verdict-heuristics.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Concise natural-language summaries with selected IDs, links, paths, and action confirmations when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute NoxInfluencer CLI commands, create or download files for exports, and preserve opaque IDs for follow-up operations.] <br>

## Skill Version(s): <br>
0.1.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
