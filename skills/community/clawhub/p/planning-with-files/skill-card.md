## Description:

Persistent file-based planning for multi-step AI-agent work. Keeps task_plan.md, findings.md, and progress.md on disk; lifecycle hooks inject selected project planning context. Automatic recovery reads project planning files only. Explicit session-catchup.py --metadata reads same-project local agent session records and emits aggregate counts only; --replay may emit bounded nonce-framed excerpts. Optional gated mode can request continuation only when the host supports it and never runs commands declared in Markdown. The skill has no network upload path. Use for research or work needing 5+ tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[othmanadi](https://clawhub.ai/user/othmanadi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to organize multi-step research or implementation work in persistent planning files, recover selected project context, and track progress across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious with medium confidence because it reports security weaknesses and unexpected behavior; analysis of some files was incomplete. This is not a finding of malicious intent.

Mitigation: Review the skill's scripts and setup instructions before installing, and install only if you need it and are comfortable with what you reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/othmanadi/skills/planning-with-files)
- [Attestation locking and fallback](https://github.com/OthmanAdi/planning-with-files/blob/master/docs/attestation-locking.md)
- [Performance notes](https://github.com/OthmanAdi/planning-with-files/blob/master/docs/perf-notes.md)
- [Claude Code hook reference](https://code.claude.com/docs/en/hooks#precompact-output)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown planning files and templates, with shell and Python helper scripts and agent setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates task plans, findings, and progress records; behavior depends on the selected plan and host lifecycle-hook support.]

## Skill Version(s):

3.28.2 (source: evidence metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
