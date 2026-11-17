## Description:

Gstack Openclaw Skills provides 15 WorkBuddy/OpenClaw agent workflows for product ideation, planning review, code review, debugging, QA, documentation, and release work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dsg12te-del](https://clawhub.ai/user/dsg12te-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill pack to route agent work through specialized workflows for ideation, planning review, code review, debugging, QA, documentation, and release preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill pack can automatically change code, install dependencies, push to remotes, create PRs, and deploy without clear final approval gates.

Mitigation: Use least-privilege repository credentials and require explicit confirmation before dependency installs, commits, pushes, PR creation, or production deployment.

Risk: Broad natural-language release triggers may route an agent into release or deployment work unintentionally.

Mitigation: Require an explicit user confirmation step before release actions and avoid ambiguous deployment requests.

Risk: The workflow state helper should not be used with untrusted workflow IDs until the path validation issue is fixed.

Mitigation: Do not pass untrusted workflow IDs to the state helper; restrict workflow IDs to trusted agent-created values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dsg12te-del/skills/gstack-openclaw-skills)
- [Original gstack project](https://github.com/garrytan/gstack)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown responses with command examples, code review findings, test reports, PR or release summaries, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform or propose repository mutations, dependency installs, commits, pushes, PR creation, and deployment when the host agent grants tools.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
