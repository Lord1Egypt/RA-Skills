## Description: <br>
OrgX operations execution contract for OpenClaw. Use for reliability, incident response, runbooks, cost controls, and rollout safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hopeatina](https://clawhub.ai/user/hopeatina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations engineers and reliability teams use this skill to shape OpenClaw agent behavior for incident response, rollout safety, runbooks, cost controls, and production change review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Operational guidance or runbooks could be applied to production changes without enough review. <br>
Mitigation: Require explicit human approval for production changes and include rollback paths, detection signals, and verification checklists. <br>
Risk: Future connections to mutation tools such as orgx_apply_changeset could expand the skill from guidance into state-changing operations. <br>
Mitigation: Grant narrow permissions and require approval, rollback support, and audit logging before enabling production mutation tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hopeatina/orgx-operations-agent) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/hopeatina) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown runbooks, checklists, operational guidance, and status or decision messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emphasizes reversible actions, rollback paths, detection signals, mitigations, and verification checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
