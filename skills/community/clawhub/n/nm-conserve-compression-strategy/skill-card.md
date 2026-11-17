## Description:

Recommends context compression strategies for bloated or quota-heavy sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to assess context bloat, choose a compression or delegation strategy, and reduce token pressure before or during long agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clearing or compacting context can lose unsaved state or recent decisions.

Mitigation: Confirm critical session state is saved before /clear, and use catchup or an archive summary to reload active context.

Risk: Pasted logs and archived session files can expose secrets or sensitive operational data.

Mitigation: Filter and redact logs before pasting, and avoid archiving secrets into .claude files.

Risk: Optional token counting can depend on third-party tooling availability and version drift.

Mitigation: Prefer a pinned or preinstalled tiktoken environment before relying on token measurements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/athola/skills/nm-conserve-compression-strategy)
- [Conserve Plugin Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve)
- [Log Debugging Hygiene Module](modules/log-debugging-hygiene.md)
- [Drain3](https://github.com/logpai/Drain3)
- [logs-tokenizer](https://github.com/sergeivaskov/logs-tokenizer)
- [LLMLingua](https://github.com/microsoft/LLMLingua)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with analysis, recommendations, estimates, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose manual session-state saves, context archiving, filtering, summarization, delegation, or continuation-agent handoff.]

## Skill Version(s):

1.9.19 (source: server release evidence; artifact frontmatter lists 1.9.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
