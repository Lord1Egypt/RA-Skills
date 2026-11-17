## Description:

Searches Chinese patent information online through Baidu or Google Patents by keyword or patent number and returns structured patent summaries and applicant data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjstrivesh](https://clawhub.ai/user/yjstrivesh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and patent analysts use this skill to search Chinese patents by keyword or CN patent number and obtain structured Markdown or JSON summaries for technical research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The npm dependency and install setup creates supply-chain risk before use.

Mitigation: Review or update the dependency chain, install from a trusted registry, and use the lockfile for reproducible installs.

Risk: Patent queries are sent to Baidu or Google Patents.

Mitigation: Use the skill only with patent queries that are acceptable to send to the selected external search provider.

Risk: The --output option writes directly to the named file path.

Mitigation: Choose output paths deliberately and review generated files before relying on or sharing them.

## Reference(s):

- [Patent Scout on ClawHub](https://clawhub.ai/yjstrivesh/skills/patent-scout)
- [Baidu Search](https://www.baidu.com/)
- [Google Patents](https://patents.google.com/)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, files]

**Output Format:** [Markdown or JSON patent search summaries, with optional file output when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live search results may be incomplete if source pages block requests, rate-limit traffic, or omit extractable patent identifiers.]

## Skill Version(s):

1.0.1 (source: evidence.release.version and target metadata; artifact files contain 1.0.0 and 2.0.0 signals)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
