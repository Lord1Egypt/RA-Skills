## Description:

Extracts character personality from novels, scripts, anime, and other source material to generate SoulPod persona packages for Memory-Inhabit dialogue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evangeliona](https://clawhub.ai/user/evangeliona)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create character persona packages from source materials for Memory-Inhabit dialogue experiences. It is suited to creative persona extraction and roleplay package generation where generated memories, prompts, and media assets can be reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate web search, downloads, dependency installation, file writes, and deployment into another skill.

Mitigation: Run it in a sandbox or disposable workspace and manually approve searches, downloads, dependency installation, and deployment steps.

Risk: Generated personas from web content may preserve untrusted or misleading prompt and memory content.

Mitigation: Inspect extracted memories, system prompts, and universal_prompt.txt before using or sharing any generated SoulPod package.

Risk: The workflow can overwrite generated output or deployed persona directories.

Mitigation: Review target paths before install steps and keep backups of existing Memory-Inhabit personas.

## Reference(s):

- [Memory Trace ClawHub Skill Page](https://clawhub.ai/evangeliona/skills/memory-trace)
- [Memory Trace Homepage](https://memory-series.github.io/#/product/trace)
- [Memory Trace README](artifact/README.md)
- [Origin Material Guide](artifact/origin/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance plus generated text, JSON configuration, prompts, memories, and asset files in a SoulPod directory.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces SoulPod packages under output/<character>/ and can install generated packages into Memory-Inhabit personas after review.]

## Skill Version(s):

1.1.7 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
