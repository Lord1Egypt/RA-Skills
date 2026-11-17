## Description:

Generates daily investment research reports for A-share, Hong Kong, and U.S. markets by collecting market data, fund flows, sector rotation, announcements, technical signals, and outlook content into structured Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolfzb](https://clawhub.ai/user/coolfzb)

### License/Terms of Use:

MIT-0

## Use Case:

External users, personal investors, and investment teams use this skill to generate daily market review reports and investment research summaries for A-share, Hong Kong, and U.S. equity markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports contain externally sourced financial content that may be incomplete, delayed, or unsuitable for investment decisions.

Mitigation: Review report content, source timestamps, and assumptions before acting on it; treat the output as research support, not financial advice.

Risk: The skill sends market queries through a local NeoData gateway and depends on network-returned market data.

Mitigation: Install only in environments where this data flow is acceptable and where the expected local gateway is available.

Risk: Generated Markdown can include externally sourced text that may be unsafe in permissive Markdown viewers.

Mitigation: Open generated Markdown in viewers that disable unsafe HTML, scripts, and external resource loading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coolfzb/skills/investment-daily-report)
- [Artifact README](artifact/README.md)
- [Artifact changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Guidance]

**Output Format:** [Markdown report files with console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports market selection, quick mode, and custom output paths; writes investment-report-YYYY-MM-DD.md by default.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact changelog lists v1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
