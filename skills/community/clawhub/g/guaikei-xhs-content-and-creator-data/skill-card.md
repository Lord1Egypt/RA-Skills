## Description:

Searches public Xiaohongshu notes, retrieves note details and comments, and collects public creator post lists for content research, competitor analysis, KOL screening, and trend discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External marketers, content operators, analysts, and creators use this skill to gather structured Xiaohongshu public-content data for topic discovery, competitor monitoring, creator evaluation, comment analysis, and market trend research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu keywords and URLs are sent to guaikei.com for data retrieval.

Mitigation: Use only when that data sharing is acceptable for the user's workflow and authorization scope.

Risk: GUAIKEI_API_TOKEN and Xiaohongshu URLs containing xsec_token values can be sensitive.

Mitigation: Keep tokens and shared URLs out of public prompts, shared terminals, and logs; rotate the API token if it is exposed.

Risk: Returned results are saved locally under logs and may contain content useful to business analysis.

Mitigation: Run in a trusted workspace and delete or protect the logs directory after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-content-and-creator-data)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei website](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Node.js CLI commands that return structured JSON, with concise guidance when inputs are missing or execution fails.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; successful calls may write returned results to a local logs directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
