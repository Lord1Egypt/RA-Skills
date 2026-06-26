## Description: <br>
Logs subagent task completions as Langfuse traces for replay, evaluation, cost analysis, backfill, tag-based filtering, and replay-judge workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to record significant subagent completions in Langfuse so sessions can be replayed, evaluated, filtered by tags, and analyzed for cost and routing decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent task prompts, outputs, and memory-derived backfill history may be persisted to Langfuse, including sensitive content. <br>
Mitigation: Use a trusted self-hosted endpoint or tightly scoped cloud project, redact sensitive data, and require explicit approval before logging sensitive sessions or running backfills. <br>
Risk: Trace logging sends data to the configured Langfuse endpoint using local credentials. <br>
Mitigation: Inspect the referenced local scripts before use, confirm the endpoint and keys, and limit Langfuse project access to intended users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/langfuse-trace-logger) <br>
- [Langfuse UI (local self-hosted endpoint)](http://localhost:3100) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with bash command examples, trace field tables, and troubleshooting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.11-compatible execution plus LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY for trace logging.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
