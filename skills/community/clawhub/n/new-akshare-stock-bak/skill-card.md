## Description:

This skill helps agents use AkShare to retrieve China A-share market data, financial data, sector information, fund-flow data, IPO data, and related stock-analysis examples.

This skill is for research and development only.

## Publisher:

[make453](https://clawhub.ai/user/make453)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to ask an agent for AkShare-based China A-share market data queries, code examples, CLI commands, and informational stock analysis. The skill states that outputs are for academic research and do not constitute investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency hygiene issues can affect AkShare-based scripts.

Mitigation: Install and run the skill only in a virtual environment, and review dependency versions before deployment.

Risk: Market-data and stock-analysis outputs can be stale, incomplete, or misleading if treated as investment advice.

Mitigation: Treat all outputs as informational, verify results against authoritative financial data sources, and avoid using the skill as a sole basis for investment decisions.

Risk: Commands and examples may fail when network access is unavailable or upstream data interfaces change.

Mitigation: Test commands in the target environment, add exception handling and retries where needed, and re-check AkShare endpoint behavior before operational use.

Risk: Some bundled examples may need fixes before use.

Mitigation: Review and lint the bundled scripts, then correct any broken API calls or missing imports before relying on their output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/make453/skills/new-akshare-stock-bak)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks; bundled CLI commands emit JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live third-party market-data APIs; outputs are informational and may fail when dependencies, network access, or upstream data interfaces change.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
