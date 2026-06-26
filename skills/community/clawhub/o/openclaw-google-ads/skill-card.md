## Description: <br>
Shared Google Ads API skill for OpenClaw agents that supports account, campaign, ad group, keyword, search term, and performance reporting with local scripts, GAQL examples, audit workflows, and read-first production-safety guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebclawops](https://clawhub.ai/user/sebclawops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to analyze authorized Google Ads accounts, run GAQL reports, audit campaign health, review wasted spend and conversion tracking, and prepare recommendations before any approved account changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth tokens, developer tokens, or account exports could expose Google Ads credentials or sensitive account data. <br>
Mitigation: Keep credentials in secure secret storage, avoid pasting refresh tokens or raw exports into chats or tracked files, and expose credentials only through approved runtime injection. <br>
Risk: Reports or recommendations may be based on the wrong Google Ads account, manager account, or date range. <br>
Mitigation: Verify account IDs, manager-account context, and date ranges before running queries or sharing findings. <br>
Risk: Operational recommendations could affect real advertising spend if converted into live account changes without review. <br>
Mitigation: Use read-only analysis by default and require separate explicit approval before pausing, enabling, editing, or changing budgets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sebclawops/openclaw-google-ads) <br>
- [API Setup](references/api-setup.md) <br>
- [Audit Workflows](references/audit-workflows.md) <br>
- [Browser Fallback](references/browser-fallback.md) <br>
- [GAQL Examples](references/gaql-examples.md) <br>
- [Optimization Heuristics](references/optimization.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with GAQL snippets, shell commands, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-first analysis posture; live Google Ads account changes require separate explicit approval.] <br>

## Skill Version(s): <br>
0.2.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
