## Description:

Protect agent memory: snapshot before compaction, scan memory/snapshot files for prompt-injection, secrets, and contradictions, audit what changed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vnbochkarev-netizen](https://clawhub.ai/user/vnbochkarev-netizen)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to snapshot agent memory before compaction, scan memory exports for prompt-injection indicators, contradictions, and anomalies, and audit changes between snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-selected memory paths and writes or prints snapshots, scan reports, and audit output that may expose sensitive content.

Mitigation: Run it only on narrow, intentional memory paths and review generated files and terminal logs before sharing them.

Risk: Secret masking is best-effort and may miss credentials outside known patterns.

Mitigation: Avoid scanning or auditing files likely to contain credentials, and treat generated artifacts as sensitive until manually reviewed.

Risk: The prompt-injection and contradiction checks are heuristic and can miss determined or unfamiliar attacks.

Mitigation: Use quarantine findings as review signals and do not treat a clean report as proof that memory is safe.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vnbochkarev-netizen/skills/memory-shield)
- [Source repository link from artifact README](https://github.com/vnbochkarev-netizen/memory-shield)
- [Sleeper memory poisoning paper referenced by artifact README](https://arxiv.org/abs/2605.15338)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports, snapshot files, terminal summaries, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated snapshots and reports may contain sensitive memory content and should be reviewed before sharing.]

## Skill Version(s):

0.1.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
