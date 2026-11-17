## Description:

Openclaw Smart Cache provides an OpenClaw smart cache with in-memory LRU and SQLite disk layers plus request-pattern learning for repeated queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[king-nan](https://clawhub.ai/user/king-nan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add local caching and request-learning patterns to OpenClaw workflows, especially for repeated API queries, database summaries, configuration reads, web fetches, and reusable computation results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cached results, query text, and request patterns may be stored locally in cache databases and log files.

Mitigation: Avoid caching secrets, keys, passwords, personal data, or sensitive business prompts unless retention behavior has been reviewed and local cache files are managed appropriately.

Risk: Cached responses can become stale for real-time or rapidly changing data.

Mitigation: Use short TTLs for volatile data, clear cache entries when needed, and avoid using this skill for workflows that require second-level freshness.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/king-nan/skills/openclaw-smart-cache)
- [Publisher profile](https://clawhub.ai/user/king-nan)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill describes local cache files, CLI management commands, TTL settings, and request-learning records.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
