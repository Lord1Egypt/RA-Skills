## Description:

Provides OpenServ Platform multi-agent workflow examples covering agent discovery, workspace orchestration, task dependencies, triggers, edges, and runnable pipeline setup patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[issa-me-sush](https://clawhub.ai/user/issa-me-sush)

### License/Terms of Use:


## Use Case:

Developers building OpenServ workflows use this skill to assemble multi-agent pipelines with marketplace agents, webhook or x402 triggers, workflow edges, dependencies, and monitoring patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples use wallet private keys and .env files, which can expose funds or account control if reused or committed.

Mitigation: Use a dedicated low-value wallet, keep secrets out of version control, and prefer a secret manager for deployed workflows.

Risk: Marketplace searches select the first matching agent in several examples, which can route sensitive work to an unreviewed third-party agent.

Mitigation: Replace first-result selection with reviewed or allowlisted agent IDs before processing sensitive, regulated, or client data.

Risk: The skill may become stale as OpenServ APIs and examples change.

Mitigation: Pin package and skill versions for repeatable builds, and review updates before adopting changed workflow behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/issa-me-sush/skills/openserv-multi-agent-workflows)
- [Multi-Agent Workflows Reference](reference.md)
- [Troubleshooting](troubleshooting.md)
- [Blog Pipeline Example](examples/blog-pipeline.md)
- [Paid Image Pipeline Example](examples/paid-image-pipeline.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript, shell, and environment variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes workflow patterns, setup examples, troubleshooting guidance, and OpenServ Platform Client usage notes.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
