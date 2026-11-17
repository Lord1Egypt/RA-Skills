## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidhov01](https://clawhub.ai/user/nidhov01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search the open skills ecosystem, compare relevant skill options, and optionally install selected skills with the Skills CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can recommend unpinned remote CLI usage and global installs that skip confirmation.

Mitigation: Review exact sources before installing found skills; prefer pinned CLI versions, immutable repository references, local installation, and visible confirmation prompts.

Risk: Installing third-party skills may add unreviewed workflows or instructions to an agent environment.

Mitigation: Review and scan selected skills before deployment, and avoid global installation unless user-level installation is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nidhov01/skills/nidhov01-find-skills)
- [Skills browser](https://skills.sh/)
- [Example Vercel React best practices skill](https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May suggest interactive search queries, install commands, and follow-up guidance when no matching skill is found.]

## Skill Version(s):

0.1.0 (source: release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
