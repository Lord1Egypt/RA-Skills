## Description: <br>
Provides integration with Redis LangCache managed service for semantic caching of prompts and responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manvinder01](https://clawhub.ai/user/manvinder01) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to add Redis LangCache semantic caching to OpenClaw workflows so repeated or similar prompts can reuse prior responses and reduce latency and API cost. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected prompts and responses may be persisted to Redis LangCache outside the local agent workflow. <br>
Mitigation: Use a least-privileged API key and avoid caching secrets, PII, regulated data, personal context, or time-sensitive content. <br>
Risk: Bypass and destructive commands can store blocked content or remove cache entries. <br>
Mitigation: Reserve --force, delete, flush, and flush-force for explicit operator-controlled maintenance after reviewing the exact data and scope. <br>


## Reference(s): <br>
- [Redis LangCache REST API Reference](references/api-reference.md) <br>
- [LangCache Best Practices](references/best-practices.md) <br>
- [Redis LangCache Documentation](https://redis.io/docs/latest/develop/ai/langcache/) <br>
- [ClawHub Skill Page](https://clawhub.ai/manvinder01/openclaw-langcache) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LangCache host, cache ID, and API key environment variables for cache operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
