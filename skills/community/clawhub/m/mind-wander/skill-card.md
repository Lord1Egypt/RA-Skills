## Description: <br>
Background reasoning agent that autonomously explores open questions using a local LLM, a private knowledge graph for dead-end tracking, and Perplexity web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jebadiahgreenwood](https://clawhub.ai/user/jebadiahgreenwood) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run scheduled background research over open questions, track dead ends, and elevate only novel findings into workspace memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can register recurring background runs that execute without direct user interaction. <br>
Mitigation: Use dry-run or manual mode first, review the schedule before enabling it, and disable cron registration if persistent execution is not acceptable. <br>
Risk: Open questions and research prompts may be sent to Perplexity web search. <br>
Mitigation: Avoid sensitive content in ON_YOUR_MIND.md and configure the Perplexity API key only in workspaces where external search is allowed. <br>
Risk: The sandbox_run tool executes local Python snippets and is not a strong security sandbox. <br>
Mitigation: Install only in a trusted workspace, review generated experiments, and do not rely on sandbox_run to isolate untrusted code. <br>
Risk: Full session transcripts and workspace context snapshots are stored in plaintext. <br>
Mitigation: Avoid sensitive inputs, restrict access to the workspace, and periodically review or delete completions/wander/ records. <br>
Risk: Gateway-token use during cron setup can expose access if copied into unsafe locations. <br>
Mitigation: Keep gateway tokens out of shared files and logs, rotate them if exposed, and prefer manual setup when token handling requirements are strict. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jebadiahgreenwood/mind-wander) <br>
- [Research Foundations](references/research.md) <br>
- [Setup & Installation](references/setup.md) <br>
- [Mind-wandering as spontaneous thought: a dynamic framework](https://doi.org/10.1038/nrn.2016.113) <br>
- [The organization of recent and remote memories](https://doi.org/10.1038/nrn1607) <br>
- [RouterRetriever: Exploring the Benefits of Routing over Multiple Expert Embedding Models](https://arxiv.org/abs/2409.02685) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, JSON session records, terminal output, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes elevated findings to MENTAL_EXPLORATION.md, records closed threads in DEAD_ENDS.md, and stores full session records under completions/wander/.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
