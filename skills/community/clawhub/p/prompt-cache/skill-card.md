## Description:

SHA-256 prompt deduplication for LLM and TTS calls -- hash normalize prompts, check cache before calling APIs, store results for instant replay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add a local cache for repeated LLM, TTS, or image generation requests, reducing duplicate API calls by hashing normalized prompts and context keys before generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private prompts, child names, language values, and generated story data may be retained in plaintext in the cache database.

Mitigation: Use a clearly scoped database with access controls, encryption or equivalent protection, and documented retention and deletion limits before caching private or child-related content.

Risk: The skill under-discloses retention of the prompt_text field and generated content.

Mitigation: Document retained fields and obtain user or operator consent, or remove prompt_text storage when plaintext prompts are not required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/prompt-cache)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and SQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local database cache guidance; no outbound network access is required by the skill evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
