## Description:

Monitors an Amazon ASIN against nearby competitors, search ranking, category bestsellers, new entrants, and review or visibility signals to produce a daily market radar with action recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pangolinfo](https://clawhub.ai/user/pangolinfo)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and commerce operators use this skill to monitor an owned ASIN, compare it with adjacent competitors, identify category movement, and decide daily defensive or counter-positioning actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use Pangolinfo API calls that consume paid credits.

Mitigation: Review the selected Fast or Full mode, expected credit use, and any budget notice before allowing the agent to continue.

Risk: The skill may write persistent ASIN baseline snapshots under ~/.pangolinfo.

Mitigation: Use it only where local product monitoring history is acceptable, and periodically review or delete stored baseline files if they are no longer needed.

Risk: The skill can propose optional daily scheduling for repeated monitoring.

Mitigation: Review any cron, n8n, or scheduler command before accepting it, including frequency, target ASINs, and credential exposure.

Risk: The skill documentation mentions API-key handling patterns that can expose credentials in URLs.

Mitigation: Prefer environment variables or Authorization headers, and avoid passing API keys in query strings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pangolinfo/skills/pangolinfo-amazon-daily-competitor-radar)
- [Pangolinfo console](https://www.pangolinfo.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with concise action recommendations and optional shell or scheduling snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain local ASIN baseline snapshots and propose optional recurring schedules.]

## Skill Version(s):

4.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
