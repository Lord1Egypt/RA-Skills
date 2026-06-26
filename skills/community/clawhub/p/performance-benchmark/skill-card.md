## Description: <br>
Measure performance baselines, detect regressions, and compare stack alternatives before and after changes across page performance, API latency, build speed, and before/after comparisons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to establish performance baselines, compare before/after changes, and catch regressions in web pages, APIs, builds, and CI workflows before release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Load tests or repeated benchmark requests could disrupt production systems or systems the user is not authorized to test. <br>
Mitigation: Run benchmarks only against local, staging, or explicitly authorized targets, and obtain team approval before testing shared or production services. <br>
Risk: Benchmark reports may include URLs, endpoint names, response details, or performance data that should not be committed or shared broadly. <br>
Mitigation: Review .benchmarks/ contents before committing, uploading artifacts, or sharing reports outside the project team. <br>
Risk: The skill does not provide its own benchmark executable, so results depend on the selected external tools and their configuration. <br>
Mitigation: Choose appropriate tools such as k6, autocannon, or hyperfine, pin versions where repeatability matters, and document the command options used for each baseline. <br>


## Reference(s): <br>
- [Benchmark Integration & Best Practices](references/integration.md) <br>
- [Benchmark Modes Detailed Reference](references/modes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/djc00p/performance-benchmark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, benchmark report examples, and CI configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to create or review .benchmarks/ baselines and reports; benchmark tools are selected and installed by the user or agent.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
