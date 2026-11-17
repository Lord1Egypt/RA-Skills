## Description:

OpenClaw Email Lead Generation helps an agent set up and operate a sales outreach pipeline with lead scoring, custom email sequences, reply monitoring, reports, and optional cron automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffjhunter](https://clawhub.ai/user/jeffjhunter)

### License/Terms of Use:

MIT

## Use Case:

External users and sales operators use this skill to manage lead records, generate tailored outreach sequences, queue or send follow-up emails with approval controls, and review pipeline reports from a conversational agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe file-writing patterns and weak automation safeguards could affect real outbound email workflows.

Mitigation: Review shell-writing and automation behavior before installation, and keep the skill in manual-send mode unless the user accepts unattended outreach risk.

Risk: Untrusted text in templates or email bodies can create unsafe or misleading outbound messages.

Mitigation: Avoid placing untrusted text directly into templates or email bodies; require user review of generated drafts before sending.

Risk: Fixed temporary files, heredoc write instructions, outside-workspace probes, and rate-limit counting need review before SMTP or cron automation.

Mitigation: Consider fixing those issues before enabling SMTP sending or cron automation, and verify rate-limit behavior in manual operation first.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jeffjhunter/skills/openclaw-email-lead-generation)
- [Template Forge reference](references/template-forge.md)
- [Lead scoring reference](references/scoring-guide.md)
- [Cron automation reference](references/cron-automation.md)
- [Publisher website](https://jeffjhunter.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational guidance with Markdown, shell command blocks, JSON/YAML configuration, and generated email drafts or templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local lead-generation files when operated by an agent; SMTP sending and cron automation are opt-in workflows.]

## Skill Version(s):

1.0.1 (source: frontmatter, artifact/_meta.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
