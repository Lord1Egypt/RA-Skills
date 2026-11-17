## Description:

Search and read Viral Loops campaign and participant data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Campaign operators use this skill to inspect connected Viral Loops campaign details, participant records, referral activity, campaign counts, and participant ranks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes unverified remote code without clearly controlling resulting changes to the computer and agent skills.

Mitigation: Install a separately verified oo CLI release, decide whether automatic skill synchronization is acceptable (OO_SKILLS_SYNC_DISABLED=1 disables it), and connect only campaigns appropriate for OOMOL to access.

## Reference(s):

- [Viral Loops](https://viral-loops.com)
- [Viral Loops API Reference](https://developers.viral-loops.com/reference/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Guidance]

**Output Format:** [Markdown text with campaign and participant information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented results from the connected campaign; participant data may be sensitive.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
