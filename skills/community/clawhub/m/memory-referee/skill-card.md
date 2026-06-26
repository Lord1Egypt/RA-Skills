## Description: <br>
Memory hygiene and adjudication layer for OpenClaw agent workflows that deduplicates entities, resolves naming conflicts, separates facts from goals from speculation, archives stale records, enforces consistent schemas, detects contradictions, and preserves provenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[honouralexwill](https://clawhub.ai/user/honouralexwill) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to clean accumulated OpenClaw memory records before passing them downstream. It helps collapse duplicates, classify records, flag contradictions, archive stale entries, and produce a reviewable adjudication result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may merge, classify, flag, or archive memory records incorrectly because parts of the adjudication are heuristic. <br>
Mitigation: Review the Markdown report and structured conflict, stale-record, and classification output before allowing it to replace or change important agent memory. <br>
Risk: Input memory records may contain sensitive or operationally important information. <br>
Mitigation: Provide only the records intended for adjudication and verify preserved provenance before using the result downstream. <br>
Risk: Staleness and contradiction decisions may miss context outside the submitted snapshot. <br>
Mitigation: Treat the output as a reviewable snapshot and compare decisions against source context when records affect ongoing goals or user preferences. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/honouralexwill/memory-referee) <br>
- [Saturnday](https://www.saturnday.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown adjudication report plus structured JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes caller-provided memory records in memory and returns a snapshot result without persistence.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata and package.json; SKILL.md frontmatter states 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
