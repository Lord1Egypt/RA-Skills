## Description:

A Chinese-language seven-stage multi-role workshop skill that helps agents clarify a task, choose role perspectives, discuss tradeoffs, produce a plan, and execute after user approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[349840432m-dev](https://clawhub.ai/user/349840432m-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to run structured multi-agent requirements, review, or planning workshops in Chinese. It creates workspace state, role cards, discussion transcripts, plan files, and deliverables under a session directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workshop files may contain sensitive project details.

Mitigation: Keep workshop directories local or redact them before sharing, publishing, or committing them.

Risk: The JD role-card helper can send role, industry, and task terms plus a Serper API key to a third-party search API.

Mitigation: Use JD search only for terms approved for external search and confirm SERPER_API_KEY handling before running the helper.

Risk: Cleanup and OpenClaw parallelism helpers can modify OpenClaw session or configuration state outside a single workshop directory.

Mitigation: Review target paths, avoid absolute or ../ role-card paths, and run these helpers only after confirming backups and intended files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/349840432m-dev/skills/multi-agent-workshop)
- [README](README.md)
- [Skill instructions](SKILL.md)
- [Anti-drift guidance](references/anti-drift.md)
- [Director forcing questions](references/director-forcing-questions.md)
- [Director supplementary rules](references/director-supplementary.md)
- [Role card from JD](references/role-card-from-jd.md)
- [Skill composition](references/skill-composition.md)
- [Subagent closure](references/subagent-closure.md)
- [gstack reference](https://github.com/garrytan/gstack)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown plans and session files with optional shell commands and JSON/configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workshop state, role cards, transcripts, plan files, and deliverables under workshops/<session_id>/.]

## Skill Version(s):

1.0.1 (source: server release metadata and claw.json; artifact SKILL.md frontmatter reports 2.2.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
