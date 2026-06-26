## Description: <br>
Captures and retrieves PR-review findings in memory palaces after PR review to store architectural decisions, patterns, and standards for future reference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill after PR reviews to decide which findings should become persistent project memory and to retrieve prior review decisions, standards, patterns, and lessons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can retain PR review content, reviewer names, file references, and architectural or security findings. <br>
Mitigation: Use it only in repositories where storing that institutional knowledge is appropriate, and review captured entries for sensitivity before retaining or sharing them. <br>
Risk: Captured review decisions, patterns, and standards can become stale or conflict with newer project guidance. <br>
Mitigation: Review the review chamber periodically, prune outdated entries, and flag contradictions when new entries are added. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-memory-palace-review-chamber) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/memory-palace) <br>
- [Capture workflow module](modules/capture-workflow.md) <br>
- [Evaluation criteria module](modules/evaluation-criteria.md) <br>
- [Search patterns module](modules/search-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, structured entry templates, scoring rubrics, and search result formats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce review-chamber entries or search summaries; no credential inputs detected.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
