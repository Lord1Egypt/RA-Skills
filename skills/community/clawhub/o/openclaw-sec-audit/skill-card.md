## Description:

Run a local security audit on the OpenClaw environment, identifying risks, affected files, and prioritized remediation steps without exposing secrets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haooyi](https://clawhub.ai/user/haooyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a local audit of OpenClaw installations and review prioritized findings about secrets, configuration, host exposure, and remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect OpenClaw config, repository files, environment files, logs, workspace memory documents, git-tracked files, and host or network state.

Mitigation: Run it in a private workspace and use opt-out flags such as --no-host or --no-git when those checks are not needed.

Risk: Generated reports may reveal host details, paths, listener information, and masked credential fragments.

Mitigation: Write reports to a directory with owner-only permissions and limit report sharing to trusted reviewers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haooyi/skills/openclaw-sec-audit)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Text, JSON, or Markdown audit report with prioritized findings and remediation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports may include host details, filesystem paths, listener information, and masked credential fragments.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
