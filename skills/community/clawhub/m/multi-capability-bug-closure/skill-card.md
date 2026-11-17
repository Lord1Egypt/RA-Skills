## Description:

Coordinates source-code review, database reads, server-log analysis, and platform queries so an agent can investigate bugs with real evidence before presenting a root-cause conclusion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use this skill to structure bug investigations around logs, database state, code paths, and platform validation. It is intended for cases where a final diagnosis should be backed by a reproducible evidence chain rather than static code review alone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may expose sensitive operational details while collecting source, log, database, and platform evidence.

Mitigation: Use least-privilege read access for each data source and review investigation outputs for sensitive data before sharing them.

Risk: A root-cause conclusion may be overstated if one of the required evidence sources is unavailable.

Mitigation: Follow the skill's capability check and report missing evidence instead of issuing a final root-cause determination when the evidence chain is incomplete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hgvgfgvh/skills/multi-capability-bug-closure)
- [server-log-analysis Skill](https://clawhub.ai/hgvgfgvh/server-log-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown bug-investigation report with evidence summaries, root-cause classification, remediation steps, and verification criteria.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include read-only query examples, log excerpts, code-path references, and a missing-evidence checklist when required capabilities are unavailable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
