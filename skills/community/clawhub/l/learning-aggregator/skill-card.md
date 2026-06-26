## Description: <br>
Learning Aggregator analyzes accumulated .learnings/ files across sessions, groups entries by pattern key, computes recurrence, and outputs ranked promotion candidates as gap reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pskoett](https://clawhub.ai/user/pskoett) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review accumulated learning logs, identify recurring gaps, and decide which patterns are ready to promote into project instructions, skills, tools, or evaluations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deep trace review can expose sensitive project context and user prompts from session transcripts. <br>
Mitigation: Use --deep only when transcript analysis is authorized; use the default .learnings-only mode for routine reporting. <br>
Risk: Gap reports may recommend promotions that are incomplete, stale, or not appropriate for a project. <br>
Mitigation: Review recommendations before changing project instructions, creating evaluations, or updating skills and tools. <br>


## Reference(s): <br>
- [Entire](https://entire.io) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown gap report with ranked patterns, evidence, and recommended actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports optional filters such as since date, minimum recurrence, area, and deep trace analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
