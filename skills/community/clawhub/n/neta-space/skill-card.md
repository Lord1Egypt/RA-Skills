## Description:

Neta Space helps agents browse Neta API spaces, worldbuilding, sub-spaces, characters, collections, and playable content by space or hashtag.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huxiuhan](https://clawhub.ai/user/huxiuhan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer questions about available Neta spaces and retrieve lore, activity, character, sub-space, collection, and gameplay details before any separate creative workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions install @talesofai/neta-skills with @latest and global package manager flags.

Mitigation: Pin a reviewed package version and prefer a local or isolated install instead of a global install.

Risk: The skill requires NETA_TOKEN for Neta CLI access.

Mitigation: Provide the token only in the intended agent environment and avoid exposing it in prompts, logs, or shared command output.

Risk: The artifact includes a command to add the separate neta-creative skill.

Mitigation: Run that add command only when the user explicitly wants content creation in addition to space browsing.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline shell commands and Neta CLI result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NETA_TOKEN and Neta CLI 0.8.0 or later.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
