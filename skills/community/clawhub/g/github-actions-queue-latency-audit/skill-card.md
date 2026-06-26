## Description: <br>
Audit GitHub Actions queue wait hotspots from run/job JSON so CI bottlenecks are visible before they stall merges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and CI maintainers use this skill to analyze exported GitHub Actions run JSON, rank queue-wait hotspots, and decide where queue latency is slowing merges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports can include internal repository names, workflow names, job URLs, branches, and run identifiers from exported GitHub Actions data. <br>
Mitigation: Run the audit on a controlled folder of exports and review generated reports before sharing or publishing them. <br>
Risk: A broad RUN_GLOB can unintentionally include private or unrelated JSON files in the audit. <br>
Mitigation: Set RUN_GLOB to a narrow path containing only the intended GitHub Actions run exports. <br>
Risk: Enabling FAIL_ON_CRITICAL can cause CI jobs to fail based on queue latency thresholds. <br>
Mitigation: Enable FAIL_ON_CRITICAL only when queue latency should intentionally gate the workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/daniellummis/github-actions-queue-latency-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Human-readable text report or machine-readable JSON, with shell command examples for collecting and running the audit] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash and python3; can exit non-zero when FAIL_ON_CRITICAL is enabled and a job reaches the critical queue threshold.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
