## Description:

Checks, summarizes, and proposes package updates across installed package managers including npm, pip, Homebrew, Cargo, and Go.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guillaumemaka](https://clawhub.ai/user/guillaumemaka)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check outdated packages, summarize update candidates, and prepare package-manager update commands for explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad update commands can change many installed tools and may affect OpenClaw or system-critical packages.

Mitigation: Review exact package-manager output before approving updates, prefer selecting individual packages, and avoid all-update commands when protected packages may be installed.

Risk: Untrusted package names could make proposed shell commands unsafe if they contain spaces, shell metacharacters, redirects, or option-like names.

Mitigation: Approve only commands built from trusted package-manager output and reject package names containing unsafe characters or option-like prefixes.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown tables with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise summaries; update commands are presented for explicit confirmation before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
