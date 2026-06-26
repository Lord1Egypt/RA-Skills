## Description: <br>
Production-ready Master Data Intelligent Matching System for matching vendor, customer, employee, and OCR-extracted records, deduplicating master data, and resolving entities across procurement, finance, sales, and HR domains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[woaim65](https://clawhub.ai/user/woaim65) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data operations teams use this skill to reconcile OCR-extracted entities with master data records, identify duplicates, route uncertain matches for human review, and produce learning payloads for future threshold tuning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive vendor, finance, sales, and HR records, including identifiers that may be confidential or personal. <br>
Mitigation: Use it only with data you are authorized to process, minimize or mask sensitive identifiers in review and learning payloads, and define retention and access controls before storing active-learning data. <br>
Risk: Low-confidence matches, field mismatches, or new information can lead to incorrect master-data updates if applied without review. <br>
Mitigation: Keep the human-in-the-loop review flow enabled for uncertain results and require reviewers to confirm, reject, create, or update records before downstream application. <br>
Risk: Active-learning threshold adjustments may drift if trained on sparse or incorrect human feedback. <br>
Mitigation: Monitor per-field error rates, require enough observations before accepting threshold changes, and periodically review adjusted thresholds against domain quality requirements. <br>


## Reference(s): <br>
- [Architecture](references/architecture.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/woaim65/master-data-matching) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples, JSON-like matching payloads, human review requests, learning statistics, and text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces confidence scores, color-coded OCR-to-schema mappings, four-state field verification results, and human-in-the-loop review actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
