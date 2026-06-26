## Description: <br>
Walks a contributor through adding a new benchmark to OpenChainBench. Covers spec format, harness contract, Prometheus scrape wiring, local validation, and PR conventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flotapponnier](https://clawhub.ai/user/flotapponnier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and contributors use this skill to add OpenChainBench benchmark specs, harnesses, Prometheus scrape jobs, and pull requests using the project conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository commands such as pnpm install, validation, development server, and build may execute project code from the OpenChainBench repository. <br>
Mitigation: Review the OpenChainBench repository before running commands and use a controlled development environment. <br>
Risk: Benchmark harnesses can depend on provider API keys and a public /metrics endpoint. <br>
Mitigation: Keep API keys in environment variables, do not commit secrets, and verify that public metrics do not expose sensitive data. <br>
Risk: Hosted harnesses can create ongoing infrastructure cost or availability obligations for contributors. <br>
Mitigation: Choose an appropriate hosting platform, monitor the harness runtime, and confirm the /metrics endpoint remains stable. <br>


## Reference(s): <br>
- [OpenChainBench repository](https://github.com/OpenChainBench/OpenChainBench) <br>
- [Propose a benchmark issue template](https://github.com/OpenChainBench/OpenChainBench/issues/new?template=new-benchmark.yml) <br>
- [OpenChainBench ideas discussions](https://github.com/OpenChainBench/OpenChainBench/discussions/categories/ideas) <br>
- [OpenChainBench Prometheus endpoint](https://prom.openchainbench.com) <br>
- [ClawHub skill page](https://clawhub.ai/flotapponnier/openchainbench-contributor) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/flotapponnier) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with YAML and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guided six-step contribution flow for benchmark specs, harnesses, Prometheus scrape configuration, validation, and pull requests.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
