## Description: <br>
Provides sanitization guidelines for external content in skills and hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to handle untrusted web, GitHub, and user-provided content safely before including it in skills, hooks, or agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may assume the referenced sanitization hook is installed automatically. <br>
Mitigation: Install and verify the source plugin separately before relying on automated sanitization; otherwise follow the checklist manually. <br>
Risk: Untrusted external content may contain prompt injection or hidden instructions. <br>
Mitigation: Treat external content as data, truncate it, strip instruction-like patterns, and wrap it in explicit boundary markers before reuse. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-content-sanitization) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with checklists and safety rules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable files are included in the scanned artifact.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
