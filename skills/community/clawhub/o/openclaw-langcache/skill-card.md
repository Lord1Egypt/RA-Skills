## Description:

Integrates Redis LangCache semantic caching into OpenClaw workflows so agents can search, store, delete, and flush cached LLM prompt-response pairs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manvinder01](https://clawhub.ai/user/manvinder01)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add Redis LangCache semantic caching to OpenClaw agents, reducing repeated LLM calls for suitable factual, documentation, template, style, and command-oriented prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected prompts and model responses may be sent to a Redis LangCache service.

Mitigation: Use the skill only with trusted LangCache endpoints and cache data that is appropriate to share with that service.

Risk: Credentials, PII, personalized responses, or policy-sensitive content could be stored if cache policy controls are bypassed.

Mitigation: Keep hard-block checks enabled, avoid shared caches for personalized or sensitive responses, and do not use the force option for secrets or PII.

Risk: Credential handling through a sourced secrets.env file may be unsuitable for production environments.

Mitigation: Use a dedicated low-privilege cache key and replace the secrets.env pattern with safer secret management before production use.

## Reference(s):

- [API Reference](references/api-reference.md)
- [Best Practices](references/best-practices.md)
- [Basic Caching Example](examples/basic-caching.sh)
- [Agent Integration Example](examples/agent-integration.py)
- [Redis LangCache documentation](https://redis.io/docs/latest/develop/ai/langcache/)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration instructions, API Calls, Guidance]

**Output Format:** [Markdown guidance with bash commands, Python examples, and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Redis LangCache host, cache ID, and API key configuration before cache operations can run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
