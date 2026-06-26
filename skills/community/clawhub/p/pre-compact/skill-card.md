## Description: <br>
Smart Compact helps OpenClaw agents scan conversation and tool-output context before compaction, extract durable details into memory files, and produce a pre-compact checklist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wavmson](https://clawhub.ai/user/wavmson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill before context compaction to preserve important facts, decisions, errors, preferences, and task progress in memory files while generating a checklist for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist broad conversation and tool-output details, including authentication-related data, into memory files. <br>
Mitigation: Require a preview of exactly what will be saved, forbid storing raw credentials, tokens, cookies, auth headers, personal data, and sensitive internal output, and redact sensitive values before writing. <br>
Risk: Saved memory logs can retain sensitive or outdated details longer than intended. <br>
Mitigation: Periodically prune or delete memory logs and keep memory writes append-only and reviewable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wavmson/pre-compact) <br>
- [Publisher Profile](https://clawhub.ai/user/wavmson) <br>
- [Memory-Dream Companion Skill](https://github.com/wavmson/openclaw-skill-memory-dream) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown checklist with memory-entry summaries and optional command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append selected details to memory/YYYY-MM-DD.md after review; requires explicit user confirmation before compaction.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
