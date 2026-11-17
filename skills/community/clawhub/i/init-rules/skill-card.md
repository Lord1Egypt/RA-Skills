## Description:

Interactively generate personalized agent rules by asking about tech stack, work style, and preferences, then writing customized rule files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to bootstrap personalized, persistent agent rules through a short interview, especially when setting up Skill Genie or refreshing universal workflow preferences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to run an unspecified setup script from an external Skill Genie dependency.

Mitigation: Install Skill Genie only from a trusted source and confirm the resolved setup.sh path before allowing execution.

Risk: The skill changes persistent agent rules that can affect future agent behavior.

Mitigation: Review existing and generated rules before applying changes, and keep the backup created before replacing the rules directory.

## Reference(s):

- [Skill Genie](https://github.com/Fei2-Labs/skill-genie)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown rule files with concise setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates skill-genie rule files and may back up an existing rules directory before applying changes.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
