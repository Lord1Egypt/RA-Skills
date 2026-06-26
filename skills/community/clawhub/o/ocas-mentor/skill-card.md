## Description: <br>
Self-improving orchestration and evaluation engine for long-running multi-skill workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigokarasu](https://clawhub.ai/user/indigokarasu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Mentor to coordinate long-running multi-skill workflows, evaluate skill performance from journals, compare champion and challenger variants, and propose skill improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent orchestration, cron jobs, and automatic updates may give the skill broad ongoing authority. <br>
Mitigation: Review or disable daily self-update and cron jobs before enabling the skill, and narrow triggers to the workflows you intend to run. <br>
Risk: The skill reads journals across OpenClaw skills and writes local state, proposals, decisions, and intake files for cooperating skills. <br>
Mitigation: Confirm which journal paths and intake directories it can access, and review generated proposals or decisions before promotion or deployment. <br>
Risk: The bundled contact-enrichment workflow can process private Gmail history and write high-confidence facts back to Weave. <br>
Mitigation: Run contact enrichment only after approving the Gmail account, target contact, message scope, extracted fields, storage location, and write-back preview. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/indigokarasu/ocas-mentor) <br>
- [README](README.md) <br>
- [Mentor Orchestration Engine](references/orchestration_engine.md) <br>
- [Mentor Evaluation Engine](references/evaluation_engine.md) <br>
- [Mentor Evolution Engine](references/evolution_engine.md) <br>
- [Mentor Workflow Plans](references/workflow_plans.md) <br>
- [Mentor Schemas](references/schemas.md) <br>
- [Journal](references/journal.md) <br>
- [Contact Enrichment Plan](references/plans/contact-enrichment.plan.md) <br>
- [Workflow Plan Template](references/plans/template.plan.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline JSON and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local project state, evaluation records, journals, workflow plans, and intake files for cooperating skills.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
