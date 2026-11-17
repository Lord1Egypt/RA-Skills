## Description:

Use JigsawStack through an OOMOL-connected account for search, text checks, suggestions, summarization, and translation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to search and work with text through JigsawStack, including checking profanity or spam, getting search suggestions, summarizing text, and translating content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI setup uses changing remote installers, and the CLI may install additional agent skills without this skill explaining those changes.

Mitigation: Install a reviewed, verified CLI release; decide whether to allow additional skill installations; review any skills before installing them. The documented OO_SKILLS_SYNC_DISABLED=1 setting can disable startup synchronization.

Risk: Text submitted to JigsawStack may be processed by OOMOL and JigsawStack.

Mitigation: Submit only content you intend both services to process.

## Reference(s):

- [JigsawStack homepage](https://jigsawstack.com)
- [JigsawStack API documentation](https://docs.jigsawstack.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [JigsawStack ClawHub listing](https://clawhub.ai/oomol/skills/oo-jigsawstack)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples; connector results are returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions use a JSON payload matched to the live connector schema.]

## Skill Version(s):

1.0.5 (source: artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
