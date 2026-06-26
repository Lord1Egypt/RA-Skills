## Description: <br>
Use when managing work with OrgX, including progress reporting, decision requests, artifact registration, memory sync, quality gates, and organization status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hopeatina](https://clawhub.ai/user/hopeatina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use OrgX to coordinate multi-agent work through structured progress reports, decision workflows, artifact registration, memory sync, quality scoring, entity management, and run control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory sync may expose sensitive local context such as MEMORY.md, daily logs, or progress summaries. <br>
Mitigation: Review local memory, daily logs, and progress summaries before syncing them to OrgX. <br>
Risk: ORGX_API_KEY is sensitive credential material. <br>
Mitigation: Keep ORGX_API_KEY in the environment and out of prompts, shared files, and generated reports. <br>
Risk: The skill depends on the external @useorgx/openclaw-plugin package. <br>
Mitigation: Install only when you trust OrgX and the external package source. <br>
Risk: Entity updates, cancellations, rollbacks, and checkpoint restores can change tracked work or run state. <br>
Mitigation: Explicitly confirm those actions before allowing an agent to perform them. <br>


## Reference(s): <br>
- [OrgX on ClawHub](https://clawhub.ai/hopeatina/orgx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tool-call examples, shell commands, configuration notes, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured guidance for reporting progress, requesting decisions, registering artifacts, syncing memory, checking quality gates, managing entities, and controlling runs.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
