## Description: <br>
Creates and refines HEARTBEAT.md files for murmur, guiding agents through an interview, draft, test, and registration flow for recurring scheduled prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wyblhl](https://clawhub.ai/user/wyblhl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up recurring agent workflows that monitor systems, repositories, pages, or research feeds and then write files, run commands, or deliver results through configured channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring autonomous agent workflows can run commands, change external accounts, or send data outside the workspace. <br>
Mitigation: Review the generated HEARTBEAT.md before testing or registering it, use scoped tokens or dedicated accounts, and prefer report-only or dry-run behavior for account changes. <br>
Risk: Relaxed execution settings such as permissions: skip or danger-full-access can increase the impact of mistakes in scheduled runs. <br>
Mitigation: Avoid those settings unless they are necessary for the specific workflow, and keep sandbox and network access as narrow as practical. <br>
Risk: Cleanup or mutation examples, including Docker pruning, can remove local resources when reused without review. <br>
Mitigation: Inspect destructive commands before use, require explicit thresholds or confirmations where possible, and know how to stop or remove the murmur daemon schedule. <br>


## Reference(s): <br>
- [Heartbeat examples](references/examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/wyblhl/heartbeat-cron) <br>
- [murmur repository](https://github.com/t0dorakis/murmur.git) <br>
- [agent-browser](https://github.com/vercel-labs/agent-browser) <br>
- [pi-browser](https://github.com/badlogic/pi-mono) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown HEARTBEAT.md drafts with YAML frontmatter and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include murmur CLI commands, scheduler settings, and delivery instructions for user-selected integrations.] <br>

## Skill Version(s): <br>
0.4.4 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
