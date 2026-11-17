## Description:

MONK-EYE Engine generates site-targeted forum research queries and report-style scaffolds for niche forum intelligence workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[balkanblbn](https://clawhub.ai/user/balkanblbn)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to prepare forum-specific research queries and draft strategic report-style outputs from niche community sources. Review is required before operational use because server security evidence flags misleading deep-crawling claims, high-risk source targeting without guardrails, and unsafe fixed-path configuration reads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes broad deep-research and large-scale crawling claims that server security evidence says are misleading.

Mitigation: Treat outputs as query planning and report scaffolding unless runtime evidence proves actual source collection, filtering, and attribution.

Risk: The configured sources include high-risk forums and do not define explicit topic, depth, source, or safety limits.

Mitigation: Set explicit allowed sources, topics, recursion depth, and review criteria before using generated queries or reports.

Risk: The scripts read configuration from fixed paths outside the package-local skill directory.

Mitigation: Correct configuration loading to use package-local files and validate paths before installation or execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/balkanblbn/skills/monk-eye-engine)
- [ClawHub publisher profile](https://clawhub.ai/user/balkanblbn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or terminal text, with optional JSON search-query lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit status logs, generated site-specific search queries, and report-style summaries; source attribution and depth claims require reviewer validation.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact/package.json, and artifact/monk_eye_config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
