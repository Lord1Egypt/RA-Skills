## Description: <br>
Run Paperclip locally for agent orchestration, AI company setup, and OpenClaw, Codex, or Claude control-plane operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Paperclip to set up and run a local control plane for AI agent companies, including adapter selection, OpenClaw integration, issue tracking, approvals, budgets, and heartbeats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can create or update Paperclip companies, issues, approvals, or heartbeats. <br>
Mitigation: Review CLI/API commands before running them and confirm the target Paperclip API base and company context. <br>
Risk: Memory and configuration files may reference operational details or environment names. <br>
Mitigation: Keep tokens and provider keys out of memory files and review saved Paperclip notes periodically. <br>
Risk: Configured adapters can send operational data to Paperclip, OpenClaw, and selected model providers. <br>
Mitigation: Use only trusted deployments and provider accounts, and enable adapters only for runtimes the operator authorizes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/paperclip) <br>
- [Paperclip homepage](https://clawic.com/skills/paperclip) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local configuration paths, environment variable names, and commands for Paperclip, OpenClaw, Codex, or Claude adapters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
