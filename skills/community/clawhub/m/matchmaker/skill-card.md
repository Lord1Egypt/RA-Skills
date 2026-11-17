## Description:

AI Matchmaker powered by real social media data: two people scan their accounts, and the agent cross-analyzes interests, values, lifestyle, aesthetics, and social habits to generate a compatibility report with a match score, chemistry points, friction warnings, and date suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sophie-xin9](https://clawhub.ai/user/sophie-xin9)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to compare two consenting people's social-media data and produce a human-readable compatibility report for relationship reflection, entertainment, and date planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to collect broad logged-in social-media profile data for two people and retain the raw data locally.

Mitigation: Use only with explicit consent from each account owner, prefer a dedicated browser profile with minimal logged-in accounts, and delete matchmaker-data after use when raw data should not be retained.

Risk: The skill can automatically set up an unpinned ManoBrowser dependency.

Mitigation: Review and pin the dependency before installation or execution.

Risk: Browser connection setup can involve endpoints and API keys.

Mitigation: Avoid passing API keys on the command line or to untrusted endpoints.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sophie-xin9/skills/matchmaker)
- [Publisher Profile](https://clawhub.ai/user/sophie-xin9)
- [ManoBrowser Dependency](https://github.com/ClawCap/ManoBrowser)
- [Example Compatibility Report](examples/xiaokai_match_report.md)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance, Configuration, Shell commands]

**Output Format:** [Markdown compatibility report with scores, narrative analysis, warnings, and date suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also guide local browser setup and profile-data collection before producing the report.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
