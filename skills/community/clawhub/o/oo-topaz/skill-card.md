## Description:

Use a connected Topaz account to submit image and video processing requests, inspect jobs, and manage results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Topaz users can submit image and video enhancement jobs, review job status and credit usage, retrieve results, and manage requests through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded code whose release was not verified and may add agent skills without explaining the changes.

Mitigation: Install a verified oo CLI release yourself, decide whether its additional agent skills are wanted, and use the documented OO_SKILLS_SYNC_DISABLED=1 setting to disable startup skill synchronization if appropriate.

Risk: OOMOL mediates access to the connected Topaz account, and operations can involve processing costs or deletion targets.

Mitigation: Consider the account trust relationship, review processing costs, and check the exact target before deleting records or stored files.

## Reference(s):

- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)
- [Topaz homepage](https://www.topazlabs.com)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files]

**Output Format:** [Shell commands and JSON payloads with Markdown summaries, job details, and result links; processed image or video files may be returned.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result download links may be temporary; follow the returned expiry information.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
