## Description: <br>
Helps agents audit and harden prompts, system prompts, SOUL.md, AGENTS.md, and cron prompts so LLMs follow rules and tool constraints more reliably. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to diagnose recurring instruction-following failures and apply prompt-hardening patterns before deploying or updating agent prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt-hardening recommendations can introduce incorrect, overbroad, or misleading constraints if applied without review. <br>
Mitigation: Review rewritten prompts before deployment and test them against representative instruction-following failures. <br>
Risk: The audit helper reads a prompt file selected by the operator. <br>
Mitigation: Run the audit helper only on prompt files you intentionally choose and avoid passing files that contain unnecessary sensitive content. <br>
Risk: Publisher identity may matter because the artifact author claim differs from the server-resolved publisher handle. <br>
Mitigation: Use the server-resolved publisher profile and verify the OpenClaw Team author claim if it affects trust or deployment approval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/prompt-hardening-v2) <br>
- [Prompt Hardening Patterns](references/patterns.md) <br>
- [Prompt Hardening Research Sources](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with checklist items and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advisory prompt-hardening recommendations; prompt changes should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
