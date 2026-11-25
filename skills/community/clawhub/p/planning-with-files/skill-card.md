## Description:

Persistent file-based planning for multi-step AI-agent work, with lifecycle hooks that restore selected project planning context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[othmanadi](https://clawhub.ai/user/othmanadi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users can use the skill to maintain plans, findings, and progress across multi-step research or implementation work, including after context changes or compacting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lifecycle hooks can place project planning content into agent context; the security review flags risks from untrusted content and reports only partial inspection of the listed components.

Mitigation: Treat injected planning content as data, keep external research in findings.md, and inspect the selected plan files before enabling hooks.

Risk: The security review flags possible unsafe selection or modification of project plan files.

Mitigation: Pin the intended plan when multiple plans exist, confirm the resolved plan directory, and review file changes before accepting them.

Risk: The security review flags possible silent replacement of existing loop instructions.

Mitigation: Check the destination and review existing loop instructions before installing the provided template.

## Reference(s):

- [Planning with Files on ClawHub](https://clawhub.ai/othmanadi/skills/planning-with-files)
- [Publisher profile: othmanadi](https://clawhub.ai/user/othmanadi)
- [Manus: Context Engineering for AI Agents](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- [Attestation locking and fallback](https://github.com/OthmanAdi/planning-with-files/blob/master/docs/attestation-locking.md)
- [Performance notes](https://github.com/OthmanAdi/planning-with-files/blob/master/docs/perf-notes.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown planning files with shell command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates planning files in the selected project plan directory; host support determines available lifecycle behavior.]

## Skill Version(s):

3.29.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
