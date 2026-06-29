## Description: <br>
Captures and retrieves PR-review findings in memory palaces so architectural decisions, recurring patterns, standards, and lessons can be reused in future reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering reviewers use this skill after pull request reviews to capture durable review knowledge, classify it into review-chamber rooms, and retrieve related decisions or patterns during later work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PR review discussions, participant names, file references, and architectural decisions may be saved in persistent searchable memory. <br>
Mitigation: Use approved storage locations and avoid capturing sensitive security details or private business context unless that storage location is approved. <br>
Risk: Outdated or contradictory captured review knowledge could mislead later code review decisions. <br>
Mitigation: Review entries periodically, prune stale guidance, maintain links, and flag contradictions when new entries conflict with existing knowledge. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-memory-palace-review-chamber) <br>
- [Memory Palace homepage](https://github.com/athola/claude-night-market/tree/master/plugins/memory-palace) <br>
- [Capture workflow module](modules/capture-workflow.md) <br>
- [Evaluation criteria module](modules/evaluation-criteria.md) <br>
- [Search patterns module](modules/search-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline YAML, bash, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide creation, search, listing, viewing, and export of review-chamber entries; exports may be markdown or JSON when supported by the surrounding memory-palace tools.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
