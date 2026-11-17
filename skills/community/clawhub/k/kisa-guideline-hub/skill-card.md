## Description:

Automatically collect security guidelines from KISA and Boho/KRCERT and publish them to Notion, including PDF attachments for Boho guidelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rebugui](https://clawhub.ai/user/rebugui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security operations teams use this skill to collect Korean security guideline publications from KISA and Boho/KRCERT and publish them into a configured Notion guideline database. It supports manual collection, full publish runs, and unattended scheduling when local credentials and dependencies are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Notion credentials and writes directly to a configured Notion database.

Mitigation: Use a dedicated least-privilege Notion token, keep it in a skill-specific environment file, and test against a non-production Notion database before production use.

Risk: The publishing script depends on unbundled code from a sibling security-news-feed skill.

Mitigation: Review and verify the sibling skill code and its dependencies before running collection or publishing commands.

Risk: Unattended scheduling can repeatedly publish or mispublish guideline content if configuration or duplicate handling is wrong.

Mitigation: Do not enable LaunchAgent or cron automation until logging, duplicate handling, and a rollback or disable path have been tested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rebugui/skills/kisa-guideline-hub)
- [KISA guideline source](https://xn--3e0bnl907agre90ivg11qswg.xn--3e0b707e/2060207)
- [Boho/KRCERT source](https://www.boho.or.kr)
- [Notion database schema for guidelines](artifact/references/schema.md)
- [Example guideline publications](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Notion database entries and uploaded PDF file blocks when executed in a configured environment.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
