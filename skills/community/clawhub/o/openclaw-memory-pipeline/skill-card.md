## Description: <br>
Install, repair, and validate a persistent Markdown memory workflow for OpenClaw-style agents using structured memory files and recurring cron jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Maiusless](https://clawhub.ai/user/Maiusless) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install, repair, and audit a local Markdown memory pipeline for OpenClaw-style agents. It helps define what should be remembered, initialize workspace memory files, create or review cron-based archive and summary jobs, and verify the pipeline is functioning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent local memory across sessions, which can retain sensitive or unwanted information. <br>
Mitigation: Review MEMORY.md and memory/ regularly, keep capture curated, and avoid storing secrets or sensitive personal data. <br>
Risk: Recurring cron jobs can continue updating memory files after setup. <br>
Mitigation: Confirm the workspace path before enabling jobs, check cron status during verification, and disable or remove the jobs when persistent memory is no longer wanted. <br>
Risk: A noisy or overly broad memory policy can promote temporary details into long-term memory. <br>
Mitigation: Use the concise memory rules, summarize instead of copying full transcripts, and reserve MEMORY.md for durable preferences, decisions, projects, and rules. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Maiusless/openclaw-memory-pipeline) <br>
- [Publisher Profile](https://clawhub.ai/user/Maiusless) <br>
- [Directory Layout](references/directory-layout.md) <br>
- [Memory Rules](references/memory-rules.md) <br>
- [Cron Spec](references/cron-spec.md) <br>
- [Verification](references/verification.md) <br>
- [Migration and Repair](references/migration-and-repair.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python scripts and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local memory files and cron configuration guidance; verification scripts print human-readable pass, warn, and fail results.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
