## Description: <br>
Prompt Cache provides SHA-256 prompt deduplication for LLM and TTS calls by normalizing prompts, checking a local cache before calling APIs, and storing results for reuse. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to add a local prompt/result cache that avoids repeated LLM, TTS, or image generation API calls when inputs and context keys repeat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cache keys or records may include child names or other personal identifiers. <br>
Mitigation: Use opaque IDs or hashes for personal identifiers, set retention limits, and apply access controls to the backing cache database. <br>
Risk: Underspecified cache keys can reuse generated content in the wrong model, language, voice, or user context. <br>
Mitigation: Include all material context fields in the cache key and adapt the key schema for each API domain. <br>


## Reference(s): <br>
- [Prompt Cache on ClawHub](https://clawhub.ai/nissan/prompt-cache) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and SQL snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local cache operations only; no outbound network calls declared.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
