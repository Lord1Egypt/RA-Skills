## Description:

Work with Promptfoo for local, repeatable LLM evaluations and red-team testing of prompts, providers, RAG systems, agents, and API-backed workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[south-american-cowboy](https://clawhub.ai/user/south-american-cowboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, validate, run, and troubleshoot Promptfoo evaluation and red-team workflows for LLM applications. It helps convert prompt, provider, RAG, agent, and API-backed systems into repeatable quality and security tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Promptfoo commands are often shown as npx promptfoo@latest, which can execute a mutable package with the user's normal permissions.

Mitigation: Use a pinned Promptfoo version or a lockfile-backed local dependency before running eval or red-team commands.

Risk: Eval and red-team workflows may access workspace files, API credentials, model providers, and network targets.

Mitigation: Run in a scoped workspace and expose only the files, API keys, providers, and network endpoints required for the specific test.

Risk: Large provider or test fan-out can increase cost, latency, and rate-limit failures.

Mitigation: Start with a small provider set and narrow test sample, then cap concurrency before broader runs.

## Reference(s):

- [Promptfoo config patterns](references/config-patterns.md)
- [Promptfoo example notes](references/example-notes.md)
- [Promptfoo config schema](https://promptfoo.dev/config-schema.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown with YAML, bash, and Python code blocks; helper scripts can produce promptfooconfig.yaml files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend Promptfoo CLI commands and scoped local helper-script execution.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
