## Description: <br>
Daily incremental update of HIPPOCAMPUS.md - domain-filtered 14-day rolling context for all agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[comicsansbestfont](https://clawhub.ai/user/comicsansbestfont) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent operators use this skill to refresh an agent-specific HIPPOCAMPUS.md from local OpenClaw memory, event, registry, and workspace sources. It keeps rolling context, open threads, commitments, and domain-specific sections current while enforcing each agent's domain boundary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and updates local OpenClaw context files for agent memory sync, including persistent HIPPOCAMPUS.md, memory entries, and .learnings archives. <br>
Mitigation: Run it only in intended workspaces and periodically review HIPPOCAMPUS.md, dated memory entries, and .learnings archives for sensitive, stale, or inaccurate content. <br>
Risk: Registry paths and domain sources control which local context is read and carried forward. <br>
Mitigation: Review registry paths before use and keep each agent's track and exclude lists scoped to the intended domain. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/comicsansbestfont/hippocampus-sync) <br>
- [Publisher Profile](https://clawhub.ai/user/comicsansbestfont) <br>
- [Agent Domain Registry](references/agent-registry.md) <br>
- [Domain-Specific Section Definitions](references/domain-sections.md) <br>
- [Hippocampus Entry Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or updates HIPPOCAMPUS.md and may append local memory entries when material changes are found.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
