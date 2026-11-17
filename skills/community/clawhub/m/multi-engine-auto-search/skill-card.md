## Description:

Aggregates search results by automatically discovering installed search skills, running them in parallel, deduplicating URLs, and falling back to Bing when no local engine returns results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chn012cjus](https://clawhub.ai/user/chn012cjus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run a query across locally installed search engines and receive a consolidated result list with source snippets for research or fact-finding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically runs broadly discovered local search scripts with the user's agent privileges and weak isolation.

Mitigation: Use it only in environments where installed search skills in the scanned OpenClaw directories are trusted; prefer an explicit allowlist or per-engine confirmation.

Risk: Sensitive queries may be exposed through Bing fallback or local temporary file handling.

Mitigation: Avoid sensitive queries, review network fallback behavior before use, and prefer secure per-run temporary files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chn012cjus/skills/multi-engine-auto-search)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Plain text / Markdown-style search summary with source list and URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Aggregates unique URLs from discovered search skills and includes source labels when available.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
