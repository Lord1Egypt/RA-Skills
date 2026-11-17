## Description:

Builds expert, domain-bounded patent search configurations with topic anchors and noise filters, validates branch precision through sampling, and exports the candidate pool and branch queries used by downstream patent panorama analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Patent analysts and agent users use this skill as the first stage of a patent panorama workflow to translate a business or technology question into audited patent search queries, a clean candidate pool, lightweight core recall, and a SaaS-ready technology taxonomy. It is intended to prepare handoff files for downstream statistics, profiling, tagging, and value analysis stages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions use an unpinned executable installer and a mutable GitHub branch, so the installed content can change between review and use.

Mitigation: Review and pin the installer package version and source commit before installing.

Risk: The workflow depends on PatSnap/Zhihuiya MCP authorization and generates patent-search handoff files in the session or project workspace.

Mitigation: Run from a restricted, non-privileged environment and confirm MCP authorization scope before generating outputs.

## Reference(s):

- [Query and Taxonomy Methodology](references/query-and-taxonomy-methodology.md)
- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/patent-panorama-insights-search)
- [Open Platform marketplace listing](https://open.zhihuiya.com/marketplace/skill-hub/patent-panorama-insights-search)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [JSON, CSV, and plain text handoff files with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mandatory outputs include run_config.json, search_config.json, candidate_pool.csv, core_recall.csv, tech_taxonomy.txt, and report_manifest.json.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
