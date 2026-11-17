## Description:

Audit GitHub Actions workflow permission scope drift to enforce least-privilege token access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and security engineers use this skill to audit GitHub Actions workflows for broad GITHUB_TOKEN permissions, missing explicit permissions policies, and pull_request_target workflows with write access before promoting CI policy changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The lightweight workflow parser can miss valid GitHub Actions syntax while the skill offers CI gate behavior.

Mitigation: Treat results as triage, review parser behavior against your workflow patterns, and avoid relying on FAIL_ON_CRITICAL as the only security control until parsing is hardened or replaced.

Risk: Permission audit findings can be incomplete or misleading if workflow filters, event filters, or permission filters are misconfigured.

Mitigation: Run the audit with reviewed filter settings and pair the output with human review or repository policy controls before enforcing changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daniellummis/skills/github-actions-permission-scope-audit)
- [Publisher Profile](https://clawhub.ai/user/daniellummis)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text report or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can exit nonzero when FAIL_ON_CRITICAL=1 and critical workflows are found.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
