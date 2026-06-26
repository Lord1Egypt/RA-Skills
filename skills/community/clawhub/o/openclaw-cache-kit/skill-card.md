## Description: <br>
Automatically apply Claude prompt caching optimizations to OpenClaw using cacheRetention long, a 59-minute heartbeat, cache-ttl pruning, and CRON.md separation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifeissea](https://clawhub.ai/user/lifeissea) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to apply and verify local caching settings intended to reduce Claude API input-token costs. It is suited for users who want scripted configuration changes plus a savings report based on OpenClaw cache trace logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The apply script changes the user's global OpenClaw defaults and attempts to restart the OpenClaw gateway. <br>
Mitigation: Review the configuration changes before running the script, keep the generated backup path, and restore from backup if the new defaults are not suitable. <br>
Risk: Enabling cache diagnostics can create local cache-trace logs that may contain sensitive operational details. <br>
Mitigation: Inspect ~/.openclaw/logs/cache-trace.jsonl after diagnostics are enabled and apply local retention, access-control, or deletion practices appropriate for the environment. <br>


## Reference(s): <br>
- [OpenClaw Cache Kit on ClawHub](https://clawhub.ai/lifeissea/openclaw-cache-kit) <br>
- [OpenClaw prompt caching optimization guide](https://slashpage.com/thomasjeong/36nj8v2wq5zqj25ykq9z) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash commands and local script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OpenClaw configuration edits, a timestamped backup path, gateway restart status, and cache savings summaries when its scripts are run.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
