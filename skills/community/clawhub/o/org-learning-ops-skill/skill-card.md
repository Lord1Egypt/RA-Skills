## Description: <br>
Analyzes full OpenClaw session history, prepares daily skill inventory assignments, and produces CEO learning briefs with a hot-skills radar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangluckybao-lab](https://clawhub.ai/user/huangluckybao-lab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Organization leaders and agent administrators use this skill to turn multi-agent collaboration logs into evidence-backed learning briefs, skill recommendations, and daily Agent x Skill assignment decisions. It supports governance workflows where installs, updates, configuration changes, and production activation require approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reviews OpenClaw session logs and agent configuration data that may contain sensitive organizational information. <br>
Mitigation: Use it only in intended admin or governance contexts and limit analysis to the agents, sessions, and configurations approved for review. <br>
Risk: The skill can recommend skill installs, updates, activations, and configuration changes that may alter agent behavior. <br>
Mitigation: Require human approval before applying installs, updates, activations, or configuration changes, and retain rollback points for each recommendation. <br>
Risk: External skill radar results may include suspicious or poorly matched skills. <br>
Mitigation: Keep suspicious candidates in a pending approval list with risk notes and do not promote them to active use until approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangluckybao-lab/org-learning-ops-skill) <br>
- [README](artifact/README.md) <br>
- [Daily brief example](artifact/examples/daily-brief-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown daily brief with coverage reports, ranked lists, decision panels, and Agent x Skill assignment tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations are expected to include evidence, risk notes, approval status, and rollback points.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
