## Description:

Convert Mercurial (hg) repositories to Git while preserving history, branches, and tags during VCS migration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poeticflowerhome](https://clawhub.ai/user/poeticflowerhome)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to migrate legacy Mercurial repositories into Git repositories, including author mapping and post-conversion verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The conversion scripts may automatically install or run external hg-fast-export tooling.

Mitigation: Preinstall and pin a trusted hg-fast-export version before running conversion commands.

Risk: A large-repository conversion script can delete an existing destination repository path without confirmation.

Mitigation: Use a fresh empty target directory and back up important data before running the scripts.

Risk: The scripts may change system packages or leave downloaded tooling under the user's home directory.

Mitigation: Review install behavior in advance and run the conversion in a controlled environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/poeticflowerhome/skills/hg-to-git)
- [hg-fast-export](https://github.com/frej/fast-export)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository paths, author-map guidance, conversion commands, and verification commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
