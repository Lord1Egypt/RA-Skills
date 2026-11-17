## Description:

Scrape and analyze OpenClaw JSONL session logs to reconstruct and backfill agent memory files with optional LLM narrative summaries and automatic secret sanitization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mpesavento](https://clawhub.ai/user/mpesavento)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to compare session logs against memory files, backfill missing daily memory, summarize session activity, and validate continuity after model switches or memory gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads private OpenClaw session history and may process sensitive conversation content.

Mitigation: Use dry-run or simple extraction first, review generated memory before relying on it, and use OpenAI or Anthropic backends only when session content is acceptable to send to those providers.

Risk: Automated backfill can create or update persistent agent memory from generated summaries.

Mitigation: Avoid unattended cron until the output is trusted, review memory files after generation, and use overwrite and preserve options deliberately.

Risk: Secret redaction is pattern-based and may not cover every uncommon credential format.

Mitigation: Treat built-in sanitization as defense in depth, review outputs for sensitive content, and avoid processing logs that contain secrets when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mpesavento/skills/memory-sync)
- [Secret pattern detection strategy](artifact/SECRET_PATTERNS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Analysis]

**Output Format:** [CLI text, Markdown memory files, and optional JSON exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or update local memory files and state used for incremental backfill.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
