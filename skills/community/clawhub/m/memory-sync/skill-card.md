## Description: <br>
Scrape and analyze OpenClaw JSONL session logs to reconstruct and backfill agent memory files, with simple extraction, optional LLM summaries, and automatic secret sanitization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mpesavento](https://clawhub.ai/user/mpesavento) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to compare session history against memory files, backfill missing or sparse daily memory, and maintain continuity after model switches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local chat history may be converted into persistent memory files that are incomplete, overly broad, or not yet reviewed. <br>
Mitigation: Start with compare or --dry-run and review generated files before relying on them. <br>
Risk: Optional LLM summarization may send sanitized session context and preserved notes to the configured OpenClaw, OpenAI, or Anthropic backend. <br>
Mitigation: Use remote summarization only when that data flow is acceptable; use simple extraction when it is not. <br>
Risk: Automated cron or incremental backfills can repeatedly update memory files before the user trusts the output. <br>
Mitigation: Avoid cron until manual runs have been reviewed and the generated memory format is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mpesavento/memory-sync) <br>
- [Secret Pattern Detection Strategy](artifact/SECRET_PATTERNS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [CLI output and generated Markdown memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run in dry-run, compare, extraction, validation, and backfill modes; optional summarization can use OpenClaw, OpenAI, or Anthropic backends.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
