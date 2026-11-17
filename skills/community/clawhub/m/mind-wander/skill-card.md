## Description:

Background reasoning agent that autonomously explores open questions using a local LLM, a private knowledge graph for dead-end tracking, Perplexity web search, sandbox experiments, and scheduled runs that write only novel findings to workspace files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jebadiahgreenwood](https://clawhub.ai/user/jebadiahgreenwood)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run autonomous background research over unresolved OpenClaw workspace questions, track dead ends, and elevate only novel findings into Markdown and session records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring autonomous execution can run background research without enough user control.

Mitigation: Review or remove the cron registration and run the agent manually until scheduling, scope, and stop controls are acceptable.

Risk: The skill can access workspace files, graph memory, local model endpoints, Perplexity, and host-level Python execution.

Mitigation: Use it only in workspaces that do not contain secrets or sensitive notes, and limit API keys and local service access to the minimum needed.

Risk: The sandbox runner is identified by security evidence as unsafe.

Mitigation: Disable or replace sandbox_run before deployment, and pin dependencies and model artifacts used by the installer.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jebadiahgreenwood/skills/mind-wander)
- [Research Foundations](references/research.md)
- [Setup & Installation](references/setup.md)
- [Mind-wandering as spontaneous thought: a dynamic framework](https://doi.org/10.1038/nrn.2016.113)
- [The organization of recent and remote memories](https://doi.org/10.1038/nrn1607)
- [RouterRetriever: Exploring the Benefits of Routing over Multiple Expert Embedding Models](https://arxiv.org/abs/2409.02685)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown findings and dead-end summaries, JSON session records, and command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes elevated findings to MENTAL_EXPLORATION.md, closed threads to DEAD_ENDS.md, and full session records under completions/wander/.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
