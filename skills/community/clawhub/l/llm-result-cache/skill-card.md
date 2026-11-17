## Description:

Tiny dependency-free TTL cache that skips a repeat LLM/API call entirely when the same input recurs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roberthill0475-lang](https://clawhub.ai/user/roberthill0475-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add a local TTL cache around expensive repeated LLM or API calls when inputs such as URLs, documents, or recurring questions appear across separate tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cached results are written to a local JSON file selected by the user, which may expose sensitive or regulated data if the file is not protected.

Mitigation: Avoid caching secrets or regulated data unless the cache file is stored with appropriate access controls and retention practices.

Risk: The default cache key uses the first positional argument, which can return an incorrect cached result when model settings, prompts, user identity, tenant, or other inputs affect the output.

Mitigation: Provide a custom key_fn that includes all inputs that materially affect the result.

Risk: The helper is single-process and reads or writes the whole JSON file on each call, so concurrent or high-throughput use can produce unreliable cache behavior.

Mitigation: Use it for occasional single-process caching, and choose a dedicated cache service for concurrent or high-volume workloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roberthill0475-lang/skills/llm-result-cache)
- [Publisher profile](https://clawhub.ai/user/roberthill0475-lang)

## Skill Output:

**Output Type(s):** [code, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local JSON cache file at the path selected by the user.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
