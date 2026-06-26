## Description: <br>
Work with Promptfoo for local, repeatable LLM evals and red-team testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[south-american-cowboy](https://clawhub.ai/user/south-american-cowboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, validate, run, and troubleshoot Promptfoo evaluation and red-team workflows for prompts, providers, RAG systems, agents, and API-backed LLM applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Promptfoo runs may send prompts, documentation, test inputs, and model outputs to configured providers or HTTP targets. <br>
Mitigation: Review generated promptfooconfig.yaml files and provider or target settings before running evaluations. <br>
Risk: Provider-backed evaluations and red-team scans can incur usage costs or expand quickly across prompts, providers, and tests. <br>
Mitigation: Start with small filtered suites, narrow provider sets, and controlled concurrency before broader runs. <br>
Risk: Credentials may be required for configured providers and could be exposed if committed with generated configs. <br>
Mitigation: Keep API keys in environment variables or local secret stores and avoid committing secrets. <br>


## Reference(s): <br>
- [Promptfoo config patterns](references/config-patterns.md) <br>
- [Promptfoo example notes](references/example-notes.md) <br>
- [Promptfoo config schema](https://promptfoo.dev/config-schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML, shell command, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated Promptfoo configuration files and preflight guidance for local evaluation workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
