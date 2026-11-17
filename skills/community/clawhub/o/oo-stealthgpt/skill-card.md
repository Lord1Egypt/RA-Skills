## Description:

StealthGPT (stealthgpt.ai). Use this skill for ANY StealthGPT request — reading, creating, and updating data. Whenever a task involves StealthGPT, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents can use this skill through a connected StealthGPT account to check text for AI detection, generate or humanize text, and inspect account balance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs a remote CLI installer, and the CLI may synchronize skills across agent homes.

Mitigation: Review and verify the CLI installation before setup; set OO_SKILLS_SYNC_DISABLED=1 before invoking it if skill synchronization is not wanted.

Risk: Text sent for detection, generation, or humanization is processed by OOMOL and StealthGPT; remote installers and live connector code remain unverified.

Mitigation: Submit only text intended for those services to process, and verify the CLI installation before allowing setup.

## Reference(s):

- [StealthGPT](https://www.stealthgpt.ai)
- [StealthGPT API authentication documentation](https://docs.stealthgpt.ai/api-reference/authentication)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON service responses and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-dependent; responses may include generated or transformed text, detection scores, or account balance data.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
