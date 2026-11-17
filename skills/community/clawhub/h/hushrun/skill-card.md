## Description:

Use before every git push in a repository that uses hushrun, when hushrun's pre-push hook refuses a push, when a line starts with "hushrun:", and when asked to set hushrun up. hushrun skips CI checks that this exact code already passed, so running them here first means CI doesn't run them again.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jccorzo](https://clawhub.ai/user/jccorzo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to check which repository checks remain before pushing, run those checks, and handle hushrun push refusals or setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions use an unpinned `npx hushrun` command that may execute a changing package version; the security scan was partial.

Mitigation: Review the setup command and confirm the intended hushrun version before running it. Inspect unresolved local references before relying on the skill.

## Reference(s):

- [hushrun release page](https://clawhub.ai/jccorzo/skills/hushrun)
- [hushrun documentation for agents](https://hushrun.com/docs/for-agents.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands depend on the repository's hushrun configuration and current release.]

## Skill Version(s):

0.11.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
