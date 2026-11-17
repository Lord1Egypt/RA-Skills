## Description:

Walks a contributor through adding a new benchmark to OpenChainBench. Covers spec format, harness contract, Prometheus scrape wiring, local validation, and PR conventions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flotapponnier](https://clawhub.ai/user/flotapponnier)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external contributors use this skill to add OpenChainBench benchmarks with a valid spec, metrics harness, Prometheus scrape configuration, local validation, and pull request conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A contributor may expose provider API keys while building or hosting a benchmark harness.

Mitigation: Keep credentials in environment variables, provide only a .env.example for local runs, and review changes before committing.

Risk: A long-running hosted harness can create operational cost or availability obligations for the contributor.

Mitigation: Review the target repository, hosting platform, harness logs, and budget before deployment, and choose a stable HTTPS host that can support continuous metrics collection.

Risk: An incomplete benchmark proposal can lead to misleading or rejected benchmark results.

Mitigation: Open the proposal issue first, document methodology and timeouts, avoid fake fallback numbers, and run the local validation commands before opening the pull request.

## Reference(s):

- [OpenChainBench GitHub Repository](https://github.com/OpenChainBench/OpenChainBench)
- [OpenChainBench Prometheus Endpoint](https://prom.openchainbench.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline YAML and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guided six-step contribution workflow for issue creation, benchmark spec authoring, harness implementation, hosting, Prometheus scrape setup, local validation, and pull request preparation.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
